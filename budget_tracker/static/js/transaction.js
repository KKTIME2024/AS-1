// 打开编辑收入模态框
function openIncomeModal(id, name, amount, description) {
    document.getElementById('editIncomeId').value = id;
    document.getElementById('editIncomeName').value = name;
    document.getElementById('editIncomeAmount').value = amount;
    document.getElementById('editIncomeDescription').value = description || '';
    
    // 设置表单的action属性指向正确的路由
    document.getElementById('editIncomeForm').action = '/edit_income/' + id;
    
    // 显示模态框
    document.getElementById('editIncomeModal').style.display = 'block';
}

// 关闭编辑收入模态框
function closeIncomeModal() {
    document.getElementById('editIncomeModal').style.display = 'none';
}

// 打开编辑支出模态框
function openExpenditureModal(id, name, amount, description, category) {
    document.getElementById('editExpenditureId').value = id;
    document.getElementById('editExpenditureName').value = name;
    document.getElementById('editExpenditureAmount').value = amount;
    document.getElementById('editExpenditureDescription').value = description || '';
    document.getElementById('editExpenditureCategory').value = category || '';
    
    // 设置表单的action属性指向正确的路由
    document.getElementById('editExpenditureForm').action = '/edit_expenditure/' + id;
    
    // 显示模态框
    document.getElementById('editExpenditureModal').style.display = 'block';
}

// 关闭编辑支出模态框
function closeExpenditureModal() {
    document.getElementById('editExpenditureModal').style.display = 'none';
}

// 页面加载完成后绑定事件监听器
document.addEventListener('DOMContentLoaded', function() {
    // 为所有收入编辑按钮添加事件监听
    const incomeEditButtons = document.querySelectorAll('.income-edit-btn');
    incomeEditButtons.forEach(button => {
        button.addEventListener('click', function() {
            const id = this.getAttribute('data-income-id');
            const name = this.getAttribute('data-income-name');
            const amount = this.getAttribute('data-income-amount');
            const description = this.getAttribute('data-income-description');
            openIncomeModal(id, name, amount, description);
        });
    });
    
    // 为所有支出编辑按钮添加事件监听
    const expenditureEditButtons = document.querySelectorAll('.expenditure-edit-btn');
    expenditureEditButtons.forEach(button => {
        button.addEventListener('click', function() {
            const id = this.getAttribute('data-expenditure-id');
            const name = this.getAttribute('data-expenditure-name');
            const amount = this.getAttribute('data-expenditure-amount');
            const description = this.getAttribute('data-expenditure-description');
            const category = this.getAttribute('data-expenditure-category');
            openExpenditureModal(id, name, amount, description, category);
        });
    });
});

// 点击模态框外部关闭窗口
window.onclick = function(event) {
    const incomeModal = document.getElementById('editIncomeModal');
    const expenditureModal = document.getElementById('editExpenditureModal');
    
    if (event.target == incomeModal) {
        closeIncomeModal();
    } else if (event.target == expenditureModal) {
        closeExpenditureModal();
    }
}