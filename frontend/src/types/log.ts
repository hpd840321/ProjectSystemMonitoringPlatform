export interface Log {
  id: string
  timestamp: string
  level: 'ERROR' | 'WARN' | 'INFO' | 'DEBUG'
  source: string
  message: string
  context: Record<string, any>
}

export interface LogListResponse {
  items: Log[]
  total: number
}

export interface LogQueryParams {
  page?: number
  pageSize?: number
  level?: string
  source?: string
  startTime?: string
  endTime?: string
  keyword?: string
} 