import ApiService from '@/services/api.service'
import { Assignment } from '@/domain/models/example/example'

export class APIAssignmentRepository {
  constructor(private readonly request = ApiService) {}

  async assign(projectId: string, exampleId: number, userId: number): Promise<Assignment | null> {
    const url = `/projects/${projectId}/assignments`
    const payload = { example: exampleId, assignee: userId }
    try {
      const response = await this.request.post(url, payload)
      return response.data
    } catch (error: any) {
      // 处理唯一性约束错误，避免阻塞界面
      if (error.response && error.response.status === 400) {
        // 检查是否是重复分配错误
        if (error.response.data.non_field_errors && 
            error.response.data.non_field_errors.includes("字段 example, assignee 必须能构成唯一集合")) {
          // 返回null表示已存在分配，不抛出错误避免阻塞
          return null
        }
      }
      // 其他错误正常抛出
      throw error
    }
  }

  async unassign(projectId: string, assignmentId: string): Promise<void> {
    const url = `/projects/${projectId}/assignments/${assignmentId}`
    await this.request.delete(url)
  }

  async bulkAssign(projectId: string, workloadAllocation: Object): Promise<void> {
    const url = `/projects/${projectId}/assignments/bulk_assign`
    try {
      await this.request.post(url, workloadAllocation)
    } catch (error: any) {
      // 处理唯一性约束错误，避免阻塞界面
      if (error.response && error.response.status === 400) {
        if (error.response.data.detail) {
          throw new Error(error.response.data.detail)
        }
      }
      throw error
    }
  }

  async reset(projectId: string): Promise<void> {
    const url = `/projects/${projectId}/assignments/reset`
    await this.request.delete(url)
  }
}