const { test, expect } = require('@playwright/test')

async function login(page, username, password) {
  await page.goto('/#/login')
  await page.getByPlaceholder('请输入用户名').fill(username)
  await page.getByPlaceholder('请输入密码').fill(password)
  await page.getByRole('button', { name: '登录' }).click()
}

test('管理员登录、主框架和权限示例', async ({ page }) => {
  await login(page, 'e2e_admin', 'E2E_Admin!234')
  await expect(page.getByText('欢迎使用 XX管理系统')).toBeVisible()
  await page.getByText('权限示例', { exact: true }).click()
  await expect(page.getByText('这是一个受角色菜单保护的示例接口。')).toBeVisible()
})

test('普通用户首次登录必须修改密码', async ({ page }) => {
  await login(page, 'e2e_user', 'E2E_Temp!234')
  await expect(page.getByText('首次登录必须先修改初始密码')).toBeVisible()
  const inputs = page.locator('.password-form input')
  await inputs.nth(0).fill('E2E_Temp!234')
  await inputs.nth(1).fill('E2E_New!2345')
  await inputs.nth(2).fill('E2E_New!2345')
  await page.getByRole('button', { name: '设置新密码' }).click()
  await expect(page).toHaveURL(/#\/login/)
  await login(page, 'e2e_user', 'E2E_New!2345')
  await expect(page.getByText('欢迎使用 XX管理系统')).toBeVisible()
  await page.goto('/#/index/example')
  await expect(page).toHaveURL(/#\/index\/dashboard/)
  const token = await page.evaluate(() => sessionStorage.getItem('token'))
  const forbidden = await page.request.get('/api/example/', { headers: { Authorization: `Bearer ${token}` } })
  expect(forbidden.status()).toBe(403)
})

test('个人资料、头像上传删除和退出登录', async ({ page }) => {
  await login(page, 'e2e_admin', 'E2E_Admin!234')
  await page.getByTestId('user-menu').click()
  await page.getByText('个人信息', { exact: true }).click()

  await page.getByTestId('profile-edit').click()
  await page.getByTestId('profile-nickname').fill('教学管理员')
  await page.getByTestId('profile-phone').fill('13800138000')
  await page.getByTestId('profile-save').click()
  await expect(page.getByText('资料保存成功')).toBeVisible()
  await expect(page.getByTestId('user-menu')).toContainText('教学管理员')

  await page.getByTestId('avatar-edit').click()
  const png = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAAFElEQVR4nGP8z8AARAwMjDAGsgAANwQCAZf6X8sAAAAASUVORK5CYII=', 'base64')
  await page.getByTestId('avatar-file').setInputFiles({ name: 'avatar.png', mimeType: 'image/png', buffer: png })
  await expect(page.locator('.avatar-dialog canvas')).toBeVisible()
  await page.getByTestId('avatar-save').click()
  await expect(page.getByText('头像保存成功')).toBeVisible()
  await expect(page.getByTestId('avatar-delete')).toBeVisible()

  await page.getByTestId('avatar-delete').click()
  await page.getByRole('button', { name: '确定' }).click()
  await expect(page.getByText('已恢复默认头像')).toBeVisible()
  await expect(page.getByTestId('avatar-delete')).toHaveCount(0)

  await page.getByTestId('user-menu').click()
  await page.getByText('退出登录', { exact: true }).click()
  await page.getByRole('button', { name: '确定' }).click()
  await expect(page).toHaveURL(/#\/login/)
  expect(await page.evaluate(() => sessionStorage.getItem('token'))).toBeNull()
})
