import io
import csv
from typing import Dict, Any, List
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt

class ReportExporter:
    """报表导出器"""

    async def export_csv(self, report: Dict[str, Any]) -> bytes:
        """导出为CSV格式"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # 写入基本信息
        writer.writerow(['Report Time Range'])
        writer.writerow(['Start Time', report['time_range']['start_time']])
        writer.writerow(['End Time', report['time_range']['end_time']])
        writer.writerow([])

        # 写入统计数据
        if 'total_stats' in report:
            writer.writerow(['Overall Statistics'])
            for key, value in report['total_stats'].items():
                writer.writerow([key, value])
            writer.writerow([])

        # 写入详细数据
        if 'servers' in report:
            writer.writerow(['Server Details'])
            # 写入表头
            headers = ['Server ID', 'Hostname'] + [
                key for key in report['servers'][0].keys()
                if key not in ['agent_id', 'hostname']
            ]
            writer.writerow(headers)
            # 写入数据
            for server in report['servers']:
                row = [server['agent_id'], server['hostname']] + [
                    server[key] for key in headers[2:]
                ]
                writer.writerow(row)

        return output.getvalue().encode('utf-8')

    async def export_excel(
        self,
        report: Dict[str, Any],
        include_charts: bool = True
    ) -> bytes:
        """导出为Excel格式"""
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # 创建概览sheet
            overview_df = pd.DataFrame({
                'Metric': list(report.get('total_stats', {}).keys()),
                'Value': list(report.get('total_stats', {}).values())
            })
            overview_df.to_excel(writer, sheet_name='Overview', index=False)
            
            # 创建详细数据sheet
            if 'servers' in report:
                servers_df = pd.DataFrame(report['servers'])
                servers_df.to_excel(writer, sheet_name='Details', index=False)
            
            # 添加图表
            if include_charts and 'trends' in report:
                chart_sheet = workbook.add_worksheet('Charts')
                
                # 创建趋势图
                for i, (metric, values) in enumerate(report['trends'].items()):
                    chart = workbook.add_chart({'type': 'line'})
                    
                    # 写入数据
                    data_sheet = workbook.add_worksheet(f'Data_{metric}')
                    data_sheet.write_column('A1', values)
                    
                    # 配置图表
                    chart.add_series({
                        'values': f'=Data_{metric}!$A$1:$A${len(values)}',
                        'name': metric
                    })
                    
                    chart.set_title({'name': f'{metric} Trend'})
                    chart.set_size({'width': 720, 'height': 400})
                    
                    # 插入图表
                    chart_sheet.insert_chart(f'A{i*25+1}', chart)

        return output.getvalue()

    async def export_pdf(
        self,
        report: Dict[str, Any],
        include_charts: bool = True
    ) -> bytes:
        """导出为PDF格式"""
        output = io.BytesIO()
        doc = SimpleDocTemplate(output, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # 添加标题
        elements.append(Paragraph('Report', styles['Title']))
        elements.append(Spacer(1, 12))

        # 添加时间范围
        elements.append(Paragraph('Time Range:', styles['Heading2']))
        time_data = [
            ['Start Time', report['time_range']['start_time']],
            ['End Time', report['time_range']['end_time']]
        ]
        time_table = Table(time_data)
        time_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('PADDING', (0, 0), (-1, -1), 6)
        ]))
        elements.append(time_table)
        elements.append(Spacer(1, 12))

        # 添加总体统计
        if 'total_stats' in report:
            elements.append(Paragraph('Overall Statistics:', styles['Heading2']))
            stats_data = [[k, v] for k, v in report['total_stats'].items()]
            stats_table = Table(stats_data)
            stats_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('PADDING', (0, 0), (-1, -1), 6)
            ]))
            elements.append(stats_table)
            elements.append(Spacer(1, 12))

        # 添加图表
        if include_charts and 'trends' in report:
            elements.append(Paragraph('Trends:', styles['Heading2']))
            
            for metric, values in report['trends'].items():
                # 创建图表
                plt.figure(figsize=(8, 4))
                plt.plot(values)
                plt.title(f'{metric} Trend')
                plt.grid(True)
                
                # 保存图表到内存
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png')
                img_buffer.seek(0)
                
                # 添加图表到PDF
                elements.append(Paragraph(f'{metric} Trend:', styles['Heading3']))
                elements.append(Image(img_buffer))
                elements.append(Spacer(1, 12))
                
                plt.close()

        # 生成PDF
        doc.build(elements)
        return output.getvalue()

report_exporter = ReportExporter() 