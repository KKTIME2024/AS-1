// 客户端表单验证
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