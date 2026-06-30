<template>
  <div class="resources-container">
    <el-card>
      <template #header>
        <div class="header">
          <h2>学习资源中心</h2>
          <div class="filters">
            <el-select
              v-model="filterType"
              placeholder="资源类型"
              @change="applyFilters"
              style="margin-right: 10px"
            >
              <el-option label="全部" value="" />
              <el-option label="文档" value="document" />
              <el-option label="视频" value="video" />
              <el-option label="代码" value="code" />
              <el-option label="练习" value="exercise" />
            </el-select>

            <el-select
              v-model="filterDifficulty"
              placeholder="难度等级"
              @change="applyFilters"
              style="margin-right: 10px"
            >
              <el-option label="全部" value="" />
              <el-option label="初级" value="beginner" />
              <el-option label="中级" value="intermediate" />
              <el-option label="高级" value="advanced" />
            </el-select>

            <el-input
              v-model="searchKeyword"
              placeholder="搜索资源..."
              @input="applyFilters"
              style="width: 200px; margin-right: 10px"
            />

            <el-button type="primary" @click="refreshResources">刷新</el-button>
          </div>
        </div>
      </template>

      <div class="resources-grid">
        <el-card
          v-for="(resource, index) in filteredResources"
          :key="index"
          class="resource-card"
          shadow="hover"
        >
          <template #header>
            <div class="card-header">
              <el-tag :type="getResourceTypeTag(resource.type)" size="small">
                {{ getResourceTypeName(resource.type) }}
              </el-tag>
              <h3>{{ resource.title }}</h3>
            </div>
          </template>

          <div class="card-content">
            <p class="resource-description">{{ resource.description }}</p>

            <div class="resource-meta">
              <el-tag :type="getResourceDifficultyTag(resource.difficulty)" size="small">
                {{ resource.difficulty }}
              </el-tag>
              <span class="meta-item">难度: {{ resource.level }}</span>
              <span class="meta-item">时长: {{ resource.duration }}分钟</span>
              <span class="meta-item">评分: {{ resource.rating }}/5</span>
            </div>

            <div class="resource-tags">
              <el-tag
                v-for="(tag, tagIndex) in resource.tags"
                :key="tagIndex"
                type="info"
                size="small"
                style="margin-right: 5px; margin-bottom: 5px"
              >
                {{ tag }}
              </el-tag>
            </div>
          </div>

          <template #footer>
            <div class="card-footer">
              <el-button type="primary" @click="viewResource(resource)">查看</el-button>
              <el-button type="info" @click="downloadResource(resource)">下载</el-button>
              <el-button type="warning" @click="addToFavorites(resource)">
                <el-icon><Star /></el-icon>
                {{ resource.isFavorite ? '取消收藏' : '收藏' }}
              </el-button>
            </div>
          </template>
        </el-card>
      </div>

      <el-pagination
        v-if="filteredResources.length > 0"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[6, 12, 24]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="filteredResources.length"
        style="margin-top: 20px; text-align: center"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Star } from '@element-plus/icons-vue'

// 模拟资源数据
const resources = ref([
  {
    id: 1,
    title: 'Python基础入门教程',
    type: 'document',
    description: '从零开始学习Python的基础语法和常用库，适合初学者。',
    difficulty: 'beginner',
    level: '初级',
    duration: 120,
    rating: 4.5,
    tags: ['Python', '基础', '编程'],
    isFavorite: false,
  },
  {
    id: 2,
    title: '机器学习实战视频',
    type: 'video',
    description: '通过实际案例学习机器学习算法的应用和实现。',
    difficulty: 'intermediate',
    level: '中级',
    duration: 180,
    rating: 4.8,
    tags: ['机器学习', '实战', '视频'],
    isFavorite: true,
  },
  {
    id: 3,
    title: '深度学习代码示例',
    type: 'code',
    description: 'TensorFlow和PyTorch的深度学习代码实现。',
    difficulty: 'advanced',
    level: '高级',
    duration: 240,
    rating: 4.9,
    tags: ['深度学习', '代码', '框架'],
    isFavorite: false,
  },
  {
    id: 4,
    title: '数据结构练习题',
    type: 'exercise',
    description: '涵盖常见数据结构的练习题和解答。',
    difficulty: 'intermediate',
    level: '中级',
    duration: 90,
    rating: 4.3,
    tags: ['数据结构', '练习', '算法'],
    isFavorite: false,
  },
  {
    id: 5,
    title: 'AI伦理与社会影响',
    type: 'document',
    description: '探讨人工智能对社会的影响和伦理问题。',
    difficulty: 'beginner',
    level: '初级',
    duration: 60,
    rating: 4.2,
    tags: ['AI伦理', '社会', '哲学'],
    isFavorite: false,
  },
  {
    id: 6,
    title: '计算机视觉项目实战',
    type: 'video',
    description: '使用OpenCV和深度学习进行计算机视觉项目的完整教程。',
    difficulty: 'advanced',
    level: '高级',
    duration: 300,
    rating: 4.7,
    tags: ['计算机视觉', 'OpenCV', '项目'],
    isFavorite: true,
  },
])

const filterType = ref('')
const filterDifficulty = ref('')
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(6)

const filteredResources = computed(() => {
  let result = resources.value

  // 类型过滤
  if (filterType.value) {
    result = result.filter((item) => item.type === filterType.value)
  }

  // 难度过滤
  if (filterDifficulty.value) {
    result = result.filter((item) => item.difficulty === filterDifficulty.value)
  }

  // 搜索过滤
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(
      (item) =>
        item.title.toLowerCase().includes(keyword) ||
        item.description.toLowerCase().includes(keyword) ||
        item.tags.some((tag) => tag.toLowerCase().includes(keyword)),
    )
  }

  // 分页
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return result.slice(start, end)
})

const getResourceTypeTag = (type) => {
  const types = {
    document: 'primary',
    video: 'success',
    code: 'warning',
    exercise: 'danger',
  }
  return types[type] || 'info'
}

const getResourceTypeName = (type) => {
  const names = {
    document: '文档',
    video: '视频',
    code: '代码',
    exercise: '练习',
  }
  return names[type] || type
}

const getResourceDifficultyTag = (difficulty) => {
  const difficulties = {
    beginner: 'success',
    intermediate: 'warning',
    advanced: 'danger',
  }
  return difficulties[difficulty] || 'info'
}

const applyFilters = () => {
  currentPage.value = 1 // 重置到第一页
}

const refreshResources = () => {
  filterType.value = ''
  filterDifficulty.value = ''
  searchKeyword.value = ''
  currentPage.value = 1
  ElMessage.success('已刷新资源列表')
}

const viewResource = (resource) => {
  ElMessage.success(`正在查看：${resource.title}`)
  // 这里可以跳转到资源详情页
}

const downloadResource = (resource) => {
  ElMessage.success(`正在下载：${resource.title}`)
  // 这里可以实现下载逻辑
}

const addToFavorites = (resource) => {
  resource.isFavorite = !resource.isFavorite
  ElMessage.success(resource.isFavorite ? '已收藏' : '已取消收藏')
}

const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1
}

const handleCurrentChange = (val) => {
  currentPage.value = val
}
</script>

<style scoped>
.resources-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filters {
  display: flex;
  align-items: center;
  gap: 10px;
}

.resources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.resource-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.card-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #1a365d;
}

.card-content {
  flex: 1;
}

.resource-description {
  color: #4a5568;
  line-height: 1.5;
  margin-bottom: 15px;
}

.resource-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 10px;
}

.meta-item {
  color: #718096;
  font-size: 0.9rem;
}

.resource-tags {
  margin-top: 10px;
}

.card-footer {
  display: flex;
  justify-content: space-around;
  gap: 10px;
}
</style>
