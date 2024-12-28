export interface BasicSettings {
  systemName: string
  adminEmail: string
  dataRetentionDays: number
}

export interface NotificationSettings {
  smtpHost: string
  smtpPort: number
  smtpUsername: string
  smtpPassword: string
  emailFrom: string
  webhookUrl: string
}

export interface StorageSettings {
  type: 'local' | 's3'
  s3Endpoint?: string
  s3AccessKey?: string
  s3SecretKey?: string
  s3Bucket?: string
}

export interface SystemSettings {
  basic: BasicSettings
  notification: NotificationSettings
  storage: StorageSettings
} 