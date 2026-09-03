<template>
  <el-dialog title="编辑头像" :visible.sync="show" width="720px" custom-class="avatar-dialog" @closed="cleanup">
    <div v-if="!imageUrl" class="dropzone" :class="{ dragging }" @click="chooseFile" @dragover.prevent="dragging = true" @dragleave.prevent="dragging = false" @drop.prevent="handleDrop">
      <i class="el-icon-upload" /><b>点击或拖放图片到这里</b><span>支持 JPEG、PNG、WebP，大小不超过 2MB</span>
    </div>
    <div v-else class="editor" tabindex="0" @keydown="handleKeydown">
      <div class="pane-title">裁剪与实时预览</div>
      <div class="canvas-wrap" @wheel.prevent="handleWheel" @pointerdown="pointerDown" @pointermove="pointerMove" @pointerup="pointerUp" @pointercancel="pointerUp"><canvas ref="canvas" width="320" height="320" /><div class="selection" /></div>
      <div class="toolbar">
        <el-button-group>
          <el-button icon="el-icon-minus" @click="zoom(-0.1)">缩小</el-button>
          <el-button icon="el-icon-plus" @click="zoom(0.1)">放大</el-button>
          <el-button icon="el-icon-refresh-right" @click="rotate">旋转</el-button>
        </el-button-group>
        <el-button @click="reset">重置</el-button>
        <el-button @click="chooseFile">重新选择</el-button>
      </div>
      <p class="tip">拖动图片调整位置，滚轮缩放；方向键微调，Shift 可加速。</p>
    </div>
    <input ref="fileInput" data-testid="avatar-file" class="hidden" type="file" accept="image/jpeg,image/png,image/webp" @change="handleFileInput">
    <span slot="footer"><el-button @click="show = false">取消</el-button><el-button data-testid="avatar-save" type="primary" :disabled="!imageUrl" :loading="saving" @click="save">保存头像</el-button></span>
  </el-dialog>
</template>

<script>
import { coverScale, keyboardOffset, nextScale } from '@/utils/avatar'

export default {
  name: 'AvatarEditor',
  props: { visible: Boolean, saving: Boolean },
  data() {
    return { image: null, imageUrl: '', scale: 1, baseScale: 1, rotation: 0, offsetX: 0, offsetY: 0, pointers: new Map(), lastDistance: 0, dragging: false }
  },
  computed: {
    show: { get() { return this.visible }, set(value) { this.$emit('update:visible', value) } }
  },
  methods: {
    chooseFile() { this.$refs.fileInput.click() },
    handleFileInput(event) { const file = event.target.files[0]; if (file) this.loadFile(file); event.target.value = '' },
    handleDrop(event) { this.dragging = false; const file = event.dataTransfer.files[0]; if (file) this.loadFile(file) },
    loadFile(file) {
      if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) return this.$message.error('仅支持 JPEG、PNG、WebP 图片')
      if (file.size > 2 * 1024 * 1024) return this.$message.error('图片不能超过 2MB')
      this.revokeUrl()
      this.imageUrl = URL.createObjectURL(file)
      const image = new Image()
      image.onload = () => { this.image = image; this.reset() }
      image.onerror = () => { this.$message.error('图片读取失败'); this.cleanup() }
      image.src = this.imageUrl
    },
    reset() {
      if (!this.image) return
      this.rotation = 0
      this.offsetX = 0
      this.offsetY = 0
      this.baseScale = coverScale(this.image.width, this.image.height)
      this.scale = 1
      this.draw()
    },
    draw() {
      if (!this.image || !this.$refs.canvas) return
      const canvas = this.$refs.canvas
      const ctx = canvas.getContext('2d')
      ctx.clearRect(0, 0, 320, 320)
      ctx.save()
      ctx.translate(160 + this.offsetX, 160 + this.offsetY)
      ctx.rotate((this.rotation * Math.PI) / 180)
      const factor = this.baseScale * this.scale
      ctx.drawImage(this.image, -this.image.width * factor / 2, -this.image.height * factor / 2, this.image.width * factor, this.image.height * factor)
      ctx.restore()
    },
    zoom(delta) { this.scale = nextScale(this.scale, delta); this.draw() },
    rotate() {
      this.rotation = (this.rotation + 90) % 360
      this.baseScale = coverScale(this.image.width, this.image.height, this.rotation)
      this.draw()
    },
    handleWheel(event) { this.zoom(event.deltaY < 0 ? 0.08 : -0.08) },
    pointerDown(event) { event.currentTarget.setPointerCapture(event.pointerId); this.pointers.set(event.pointerId, { x: event.clientX, y: event.clientY }) },
    pointerMove(event) {
      if (!this.pointers.has(event.pointerId)) return
      const previous = this.pointers.get(event.pointerId)
      this.pointers.set(event.pointerId, { x: event.clientX, y: event.clientY })
      if (this.pointers.size === 1) {
        const ratio = 320 / event.currentTarget.clientWidth
        this.offsetX += (event.clientX - previous.x) * ratio
        this.offsetY += (event.clientY - previous.y) * ratio
      } else if (this.pointers.size === 2) {
        const points = Array.from(this.pointers.values())
        const distance = Math.hypot(points[0].x - points[1].x, points[0].y - points[1].y)
        if (this.lastDistance) this.zoom((distance - this.lastDistance) / 300)
        this.lastDistance = distance
      }
      this.draw()
    },
    pointerUp(event) { this.pointers.delete(event.pointerId); if (this.pointers.size < 2) this.lastDistance = 0 },
    handleKeydown(event) {
      if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(event.key)) return
      event.preventDefault()
      const [x, y] = keyboardOffset(event.key, event.shiftKey)
      this.offsetX += x
      this.offsetY += y
      this.draw()
    },
    save() {
      const output = document.createElement('canvas')
      output.width = 320
      output.height = 320
      output.getContext('2d').drawImage(this.$refs.canvas, 32, 32, 256, 256, 0, 0, 320, 320)
      output.toBlob(blob => { if (blob) this.$emit('save', blob) }, 'image/webp', 0.9)
    },
    revokeUrl() { if (this.imageUrl) URL.revokeObjectURL(this.imageUrl) },
    cleanup() {
      this.revokeUrl()
      this.imageUrl = ''
      this.image = null
      this.pointers.clear()
      this.lastDistance = 0
      const canvas = this.$refs.canvas
      if (canvas) canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
    }
  },
  beforeDestroy() { this.cleanup() }
}
</script>

<style scoped>
.dropzone { min-height: 330px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; text-align: center; border: 2px dashed #cbd3e6; border-radius: 18px; color: var(--app-muted); background: #fafbff; cursor: pointer; transition: .2s; }
.dropzone:hover, .dropzone.dragging { border-color: var(--app-primary); background: #f1f3ff; }.dropzone i { font-size: 58px; color: var(--app-primary); }.dropzone b { color: #35405a; font-size: 18px; }.hidden { display: none; }
.editor { outline: none; }.pane-title { margin-bottom: 12px; font-weight: 600; text-align: center; }.canvas-wrap { position: relative; width: 320px; height: 320px; margin: auto; overflow: hidden; border-radius: 14px; background: #202a3b; touch-action: none; cursor: move; box-shadow: 0 8px 25px rgba(58,70,120,.22); }
canvas { width: 100%; height: 100%; display: block; }.selection { position: absolute; inset: 10%; border: 2px solid #fff; border-radius: 50%; box-shadow: 0 0 0 9999px rgba(0,0,0,.38), 0 0 0 1px var(--app-primary); pointer-events: none; }.toolbar { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-top: 22px; }.tip { text-align: center; color: var(--app-muted); font-size: 12px; }
.avatar-dialog { max-width: 96vw; }
@media (max-width: 600px) { .canvas-wrap { width: 260px; height: 260px; } }
</style>
