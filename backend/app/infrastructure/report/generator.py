from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.agent import AgentMetrics
from app.models.alert import Alert
from app.interface.api.v1.schemas.report import (
    TimeRange,
    ResourceUsageReport,
    AlertReport,
    PerformanceReport
)
from app.infrastructure.report.exporter import report_exporter

class ReportGenerator:
    """报表生成器"""

    async def generate_resource_usage_report(
        self,
        db: Session,
        time_range: TimeRange
    ) -> ResourceUsageReport:
        """生成资源使用报表"""
        # 查询时间范围内的指标数据
        metrics = db.query(AgentMetrics)\
                   .filter(
                       AgentMetrics.timestamp.between(
                           time_range.start_time,
                           time_range.end_time
                       )
                   )\
                   .all()

        # 按服务器分组统计
        servers = {}
        for metric in metrics:
            if metric.agent_id not in servers:
                servers[metric.agent_id] = {
                    "agent_id": metric.agent_id,
                    "hostname": metric.agent.hostname,
                    "cpu_usage": [],
                    "memory_usage": [],
                    "disk_usage": [],
                    "network_in": [],
                    "network_out": []
                }
            
            servers[metric.agent_id]["cpu_usage"].append(metric.cpu_usage)
            servers[metric.agent_id]["memory_usage"].append(metric.memory_usage)
            servers[metric.agent_id]["disk_usage"].append(metric.disk_usage)
            servers[metric.agent_id]["network_in"].append(metric.network_in)
            servers[metric.agent_id]["network_out"].append(metric.network_out)

        # 计算每个服务器的统计数据
        for server in servers.values():
            for key in ["cpu_usage", "memory_usage", "disk_usage", "network_in", "network_out"]:
                values = server[key]
                server[f"{key}_avg"] = sum(values) / len(values)
                server[f"{key}_max"] = max(values)
                server[f"{key}_min"] = min(values)
                server.pop(key)  # 移除原始数据

        # 计算总体统计
        total_stats = {
            "cpu_usage_avg": sum(s["cpu_usage_avg"] for s in servers.values()) / len(servers),
            "memory_usage_avg": sum(s["memory_usage_avg"] for s in servers.values()) / len(servers),
            "disk_usage_avg": sum(s["disk_usage_avg"] for s in servers.values()) / len(servers),
            "network_in_total": sum(s["network_in_avg"] for s in servers.values()),
            "network_out_total": sum(s["network_out_avg"] for s in servers.values())
        }

        # 计算趋势数据
        df = pd.DataFrame([{
            'timestamp': m.timestamp,
            'cpu_usage': m.cpu_usage,
            'memory_usage': m.memory_usage,
            'disk_usage': m.disk_usage,
            'network_in': m.network_in,
            'network_out': m.network_out
        } for m in metrics])

        trends = {}
        if not df.empty:
            df.set_index('timestamp', inplace=True)
            df = df.resample('1H').mean()  # 按小时聚合
            trends = {
                'cpu_usage': df.cpu_usage.tolist(),
                'memory_usage': df.memory_usage.tolist(),
                'disk_usage': df.disk_usage.tolist(),
                'network_in': df.network_in.tolist(),
                'network_out': df.network_out.tolist()
            }

        return ResourceUsageReport(
            time_range=time_range,
            servers=list(servers.values()),
            total_stats=total_stats,
            trends=trends
        )

    async def generate_alert_report(
        self,
        db: Session,
        time_range: TimeRange
    ) -> AlertReport:
        """生成告警报表"""
        # 查询时间范围内的告警
        alerts = db.query(Alert)\
                  .filter(
                      Alert.created_at.between(
                          time_range.start_time,
                          time_range.end_time
                      )
                  )\
                  .all()

        # 计算总数
        total_count = len(alerts)

        # 按严重程度统计
        by_severity = {}
        for alert in alerts:
            by_severity[alert.severity] = by_severity.get(alert.severity, 0) + 1

        # 按状态统计
        by_status = {}
        for alert in alerts:
            by_status[alert.status] = by_status.get(alert.status, 0) + 1

        # 按服务器统计
        by_server = {}
        for alert in alerts:
            by_server[alert.agent_id] = by_server.get(alert.agent_id, 0) + 1

        # 计算趋势
        df = pd.DataFrame([{
            'date': a.created_at.date(),
            'severity': a.severity
        } for a in alerts])

        trends = {}
        if not df.empty:
            for severity in df.severity.unique():
                severity_df = df[df.severity == severity]
                counts = severity_df.groupby('date').size()
                date_range = pd.date_range(
                    time_range.start_time.date(),
                    time_range.end_time.date()
                )
                counts = counts.reindex(date_range, fill_value=0)
                trends[severity] = counts.tolist()

        return AlertReport(
            time_range=time_range,
            total_count=total_count,
            by_severity=by_severity,
            by_status=by_status,
            by_server=by_server,
            trends=trends
        )

    async def generate_performance_report(
        self,
        db: Session,
        time_range: TimeRange
    ) -> PerformanceReport:
        """生成性能报表"""
        # 查询时间范围内的性能指标
        metrics = db.query(AgentMetrics)\
                   .filter(
                       AgentMetrics.timestamp.between(
                           time_range.start_time,
                           time_range.end_time
                       )
                   )\
                   .order_by(AgentMetrics.timestamp.asc())\
                   .all()

        # 转换为DataFrame进行分析
        df = pd.DataFrame([{
            'timestamp': m.timestamp,
            'cpu_usage': m.cpu_usage,
            'memory_usage': m.memory_usage,
            'disk_usage': m.disk_usage,
            'network_in': m.network_in,
            'network_out': m.network_out
        } for m in metrics])

        if df.empty:
            return PerformanceReport(
                time_range=time_range,
                metrics={},
                stats={},
                anomalies=[]
            )

        # 设置时间索引
        df.set_index('timestamp', inplace=True)

        # 计算性能指标
        metrics_data = {
            'cpu_usage': df.cpu_usage.tolist(),
            'memory_usage': df.memory_usage.tolist(),
            'disk_usage': df.disk_usage.tolist(),
            'network_in': df.network_in.tolist(),
            'network_out': df.network_out.tolist()
        }

        # 计算统计数据
        stats = {}
        for col in df.columns:
            stats[col] = {
                'min': df[col].min(),
                'max': df[col].max(),
                'avg': df[col].mean(),
                'std': df[col].std()
            }

        # 检测异常点
        anomalies = []
        for col in df.columns:
            mean = df[col].mean()
            std = df[col].std()
            threshold = 3  # 3个标准差
            
            anomaly_points = df[abs(df[col] - mean) > threshold * std]
            for timestamp, value in anomaly_points[col].items():
                anomalies.append({
                    'metric': col,
                    'timestamp': timestamp,
                    'value': value,
                    'threshold': mean + threshold * std
                })

        return PerformanceReport(
            time_range=time_range,
            metrics=metrics_data,
            stats=stats,
            anomalies=anomalies
        )

    async def export_report(
        self,
        report: Dict[str, Any],
        format: str,
        include_charts: bool = True
    ) -> bytes:
        """导出报表"""
        if format == 'csv':
            return await self._export_csv(report)
        elif format == 'pdf':
            return await self._export_pdf(report, include_charts)
        elif format == 'excel':
            return await self._export_excel(report, include_charts)
        else:
            raise ValueError(f"Unsupported format: {format}")

    async def _export_csv(self, report: Dict[str, Any]) -> bytes:
        """导出为CSV格式"""
        return await report_exporter.export_csv(report)

    async def _export_pdf(
        self,
        report: Dict[str, Any],
        include_charts: bool
    ) -> bytes:
        """导出为PDF格式"""
        return await report_exporter.export_pdf(report, include_charts)

    async def _export_excel(
        self,
        report: Dict[str, Any],
        include_charts: bool
    ) -> bytes:
        """导出为Excel格式"""
        return await report_exporter.export_excel(report, include_charts)

report_generator = ReportGenerator() 