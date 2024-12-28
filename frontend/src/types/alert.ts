export interface AlertRule {
  id: string
  name: string
  metric: string
  condition: string
  threshold: number
  enabled: boolean
  notifications: string[]
  created_at: string
}

export interface Alert {
  id: string
  rule: AlertRule
  target: string
  message: string
  level: 'critical' | 'warning' | 'info'
  status: 'active' | 'resolved'
  created_at: string
  resolved_at?: string
}

export interface AlertListResponse {
  items: Alert[]
  total: number
} 