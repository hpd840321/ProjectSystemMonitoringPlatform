export interface ResourceTrend {
  timestamps: string[]
  values: number[]
}

export interface ServiceStatus {
  name: string
  status: 'running' | 'warning' | 'error'
  uptime: string
}

export interface AlertStat {
  label: string
  level: 'critical' | 'warning' | 'info'
  count: number
}

export interface SystemStatus {
  servers: {
    total: number
    online: number
  }
  resources: {
    cpu: number
    memory: number
    disk: number
  }
  services: ServiceStatus[]
  alerts: AlertStat[]
} 