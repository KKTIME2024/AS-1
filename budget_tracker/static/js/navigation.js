/**
 * 导航功能增强
 * 实现移动端菜单切换、键盘导航支持、可访问性优化
 */

// 页面加载完成后执行
 document.addEventListener('DOMContentLoaded', function() {
    // 获取导航相关元素
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    
    // 移动端菜单切换功能
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            const expanded = this.getAttribute('aria-expanded') === 'true';
            this.setAttribute('aria-expanded', !expanded);
            navMenu.classList.toggle('active');
        });
        
        // 点击菜单项后关闭菜单（仅在移动端）
        const navLinks = navMenu.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth <= 768) {
                    navToggle.setAttribute('aria-expanded', 'false');
                    navMenu.classList.remove('active');
                }
            });
        });
        
        // 监听窗口大小变化，确保在桌面模式下菜单正常显示
        window.addEventListener('resize', function() {
            if (window.innerWidth > 768) {
                navToggle.setAttribute('aria-expanded', 'false');
                navMenu.classList.remove('active');
            }
        });
    }
    
    // 键盘导航支持：Tab键在菜单末尾按Tab时聚焦到菜单开始，Shift+Tab在菜单开始时聚焦到菜单末尾
    if (navMenu) {
        const navLinks = Array.from(navMenu.querySelectorAll('a'));
        const firstLink = navLinks[0];
        const lastLink = navLinks[navLinks.length - 1];
        
        if (firstLink && lastLink) {
            // 最后一个菜单项按Tab键时，聚焦到第一个菜单项
            lastLink.addEventListener('keydown', function(e) {
                if (e.key === 'Tab' && !e.shiftKey) {
                    e.preventDefault();
                    firstLink.focus();
                }
            });
            
            // 第一个菜单项按Shift+Tab键时，聚焦到最后一个菜单项
            firstLink.addEventListener('keydown', function(e) {
                if (e.key === 'Tab' && e.shiftKey) {
                    e.preventDefault();
                    lastLink.focus();
                }
            });
        }
    }
    
    // 平滑滚动效果
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            // 确保是页面内锚点链接，而不是导航到其他页面
            if (this.getAttribute('href') !== '#' && this.getAttribute('href').startsWith('#')) {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    targetElement.scrollIntoView({ 
                        behavior: 'smooth',
                        block: 'start'
                    });
                    
                    // 聚焦到目标元素，提升可访问性
                    targetElement.setAttribute('tabindex', '-1');
                    targetElement.focus();
                }
            }
        });
    });
    
    // 设置活动菜单项的aria-current属性
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-menu a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.setAttribute('aria-current', 'page');
        }
    });
});

// 添加全局错误处理
window.addEventListener('error', function(e) {
    console.error('发生错误:', e.error);
    // 可以在这里添加错误报告逻辑
});

// 确保焦点在模态框关闭后返回到触发元素
function setupModalFocusManagement(modalTrigger, modalElement, closeButton) {
    if (modalTrigger && modalElement && closeButton) {
        modalTrigger.addEventListener('click', function() {
            // 保存触发元素
            modalElement._triggerElement = this;
        });
        
        closeButton.addEventListener('click', function() {
            // 模态框关闭后，焦点返回到触发元素
            if (modalElement._triggerElement) {
                setTimeout(() => {
                    modalElement._triggerElement.focus();
                }, 100);
            }
        });
    }
}