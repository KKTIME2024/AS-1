// 打开编辑模态框
function openEditModal(id, name, targetAmount, description) {
    document.getElementById('editGoalId').value = id;
    document.getElementById('editName').value = name;
    document.getElementById('editTargetAmount').value = targetAmount;
    document.getElementById('editDescription').value = description || '';
    
    // 设置表单的action属性指向正确的路由
    document.getElementById('editGoalForm').action = '/edit_goal/' + id;
    
    // 显示模态框
    document.getElementById('editModal').style.display = 'block';
}

// 为所有编辑按钮添加事件监听
document.addEventListener('DOMContentLoaded', function() {
    const editButtons = document.querySelectorAll('.edit-btn');
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const id = this.getAttribute('data-goal-id');
            const name = this.getAttribute('data-goal-name');
            const targetAmount = this.getAttribute('data-goal-amount');
            const description = this.getAttribute('data-goal-desc');
            openEditModal(id, name, targetAmount, description);
        });
    });
});

// 关闭编辑模态框
function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}

// 点击模态框外部关闭
window.onclick = function(event) {
    var modal = document.getElementById('editModal');
    if (event.target == modal) {
        closeEditModal();
    }
}