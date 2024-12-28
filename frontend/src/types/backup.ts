export interface Backup {
  id: string
  filename: string
  size: number
  created_at: string
  created_by: string
  status: 'pending' | 'success' | 'failed'
  error_message?: string
  backup_type: 'full' | 'config' | 'database'
  metadata: Record<string, any>
}

export interface BackupRestore {
  id: string
  backup_id: string
  restored_at: string
  restored_by: string
  status: 'pending' | 'success' | 'failed'
  error_message?: string
}

export interface BackupListResponse {
  items: Backup[]
  total: number
} 