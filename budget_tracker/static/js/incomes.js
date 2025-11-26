/**
 * 收入表单验证和交互增强
 */

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 获取收入表单元素
    const incomeForm = document.querySelector('form[action="' + window.location.pathname + '/add_income"]') || document.querySelector('form[action="/add_income"]');
    const amountInput = document.getElementById('amount');
    const nameInput = document.getElementById('name');
    const descriptionInput = document.getElementById('description');
    
    // 添加表单输入事件监听器，实现实时验证
    if (amountInput) {
        // 实时金额验证
        amountInput.addEventListener('input', function() {
            validateAmountField(this);
        });
        
        // 失焦验证
        amountInput.addEventListener('blur', function() {
            validateAmountField(this);
        });
    }
    
    if (nameInput) {
        // 输入长度限制提示
        nameInput.addEventListener('input', function() {
            const maxLength = 100;
            if (this.value.length > maxLength) {
                this.value = this.value.substring(0, maxLength);
                showError(this, `名称不能超过${maxLength}个字符`);
            } else {
                removeError(this);
            }
        });
    }
    
    if (descriptionInput) {
        // 输入长度限制提示
        descriptionInput.addEventListener('input', function() {
            const maxLength = 500;
            if (this.value.length > maxLength) {
                this.value = this.value.substring(0, maxLength);
                showError(this, `描述不能超过${maxLength}个字符`);
            } else {
                removeError(this);
            }
        });
    }
    
    // 增强表单键盘导航
    if (incomeForm) {
        // Enter键在金额输入框时聚焦到下一个字段
        amountInput?.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const nextField = descriptionInput || incomeForm.querySelector('button[type="submit"]');
                if (nextField) nextField.focus();
            }
        });
        
        // 按Escape键重置表单错误状态
        incomeForm.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                const errorElements = this.querySelectorAll('.form-error');
                errorElements.forEach(el => el.remove());
                const inputElements = this.querySelectorAll('input, textarea');
                inputElements.forEach(el => el.classList.remove('error'));
            }
        });
    }
    
    // 增强类别选择的可访问性
    const categoryRadios = document.querySelectorAll('input[name="category"]');
    categoryRadios.forEach(radio => {
        // 添加键盘焦点样式增强
        radio.addEventListener('focus', function() {
            const label = this.closest('.category-tag');
            if (label) label.classList.add('focused');
        });
        
        radio.addEventListener('blur', function() {
            const label = this.closest('.category-tag');
            if (label) label.classList.remove('focused');
        });
    });
});

/**
 * 验证金额字段
 * @param {HTMLInputElement} input - 金额输入框元素
 * @returns {boolean} - 验证是否通过
 */
function validateAmountField(input) {
    // 移除之前的错误提示
    removeError(input);
    
    // 获取输入值
    const value = input.value.trim();
    
    // 检查是否为空
    if (!value) {
        showError(input, '请输入金额');
        return false;
    }
    
    // 转换为数字
    const amount = parseFloat(value);
    
    // 检查是否为有效数字
    if (isNaN(amount)) {
        showError(input, '请输入有效的金额数值');
        return false;
    }
    
    // 检查是否大于最小允许值
    const minValue = parseFloat(input.min || 0.01);
    if (amount < minValue) {
        showError(input, `金额必须大于${minValue}`);
        return false;
    }
    
    // 检查小数位数
    const decimalPlaces = (value.split('.')[1] || '').length;
    if (decimalPlaces > 2) {
        showError(input, '金额最多保留两位小数');
        return false;
    }
    
    return true;
}

/**
 * 显示错误信息
 * @param {HTMLElement} input - 输入元素
 * @param {string} message - 错误信息
 */
function showError(input, message) {
    // 检查是否已存在错误提示
    let errorElement = input.nextElementSibling;
    if (!errorElement || !errorElement.classList.contains('form-error')) {
        errorElement = document.createElement('div');
        errorElement.className = 'form-error';
        input.parentNode.insertBefore(errorElement, input.nextSibling);
    }
    
    // 设置错误信息
    errorElement.textContent = message;
    
    // 添加错误样式
    input.classList.add('error');
    
    // 增强可访问性
    input.setAttribute('aria-invalid', 'true');
    input.setAttribute('aria-describedby', errorElement.id || (errorElement.id = 'error-' + input.id));
}

/**
 * 移除错误信息
 * @param {HTMLElement} input - 输入元素
 */
function removeError(input) {
    // 查找并移除错误提示元素
    let errorElement = input.nextElementSibling;
    if (errorElement && errorElement.classList.contains('form-error')) {
        errorElement.remove();
    }
    
    // 移除错误样式
    input.classList.remove('error');
    
    // 重置可访问性属性
    input.setAttribute('aria-invalid', 'false');
    input.removeAttribute('aria-describedby');
}

/**
 * 收入表单提交验证
 * @returns {boolean} - 表单是否通过验证
 */
function validateIncomeForm() {
    // 获取表单元素
    const amountInput = document.getElementById('amount');
    let isValid = true;
    
    // 验证金额字段
    if (!validateAmountField(amountInput)) {
        isValid = false;
        // 聚焦到金额输入框
        amountInput.focus();
    }
    
    // 如果验证失败，滚动到页面顶部显示错误信息
    if (!isValid) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    return isValid;
}// 客户端表单验证
function validateIncomeForm() {
    const amount = document.getElementById('amount').value;
    
    // 检查是否为有效数字
    if (isNaN(amount) || amount === '') {
        alert('请输入有效的金额数值！');
        return false;
    }
    
    // 检查金额是否大于0
    if (parseFloat(amount) <= 0) {
        alert('错误：收入金额必须大于0！');
        return false;
    }
    
    return true;
}