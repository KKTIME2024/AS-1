// 页面加载完成后初始化图表
document.addEventListener('DOMContentLoaded', function() {
    // 从数据属性获取图表数据
    const chartDataElement = document.getElementById('chart-data');
    const totalIncome = parseFloat(chartDataElement.getAttribute('data-total-income'));
    const totalExpense = parseFloat(chartDataElement.getAttribute('data-total-expense'));
    
    // 初始化收入支出条形图
        if (totalIncome > 0 || totalExpense > 0) {
            const barCtx = document.getElementById('incomeExpenseChart').getContext('2d');
            new Chart(barCtx, {
                type: 'bar',
                data: {
                    labels: ['收入', '支出'],
                    datasets: [{
                        label: '金额',
                        data: [totalIncome, totalExpense],
                        backgroundColor: [
                            'rgba(75, 192, 192, 0.8)',
                            'rgba(255, 99, 132, 0.8)'
                        ],
                        borderColor: [
                            'rgba(75, 192, 192, 1)',
                            'rgba(255, 99, 132, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: '金额 (¥)'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    let label = context.label || '';
                                    if (label) {
                                        label += ': ';
                                    }
                                    label += '¥' + context.raw.toFixed(2);
                                    return label;
                                }
                            }
                        }
                    }
                }
            });
        }
        
        // 初始化收入按标签分类饼图
        const incomeCategories = JSON.parse(chartDataElement.getAttribute('data-income-categories'));
        const incomeAmounts = JSON.parse(chartDataElement.getAttribute('data-income-amounts'));
        if (incomeCategories && incomeCategories.length > 0) {
            const pieCtx = document.getElementById('incomeByCategoryChart').getContext('2d');
            
            // 生成饼图颜色
            const pieColors = [
                'rgba(75, 192, 192, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(153, 102, 255, 0.8)',
                'rgba(255, 159, 64, 0.8)',
                'rgba(199, 199, 199, 0.8)',
                'rgba(83, 102, 255, 0.8)',
                'rgba(255, 99, 132, 0.8)'
            ];
            
            // 为每个类别生成颜色，如果类别数量超过预定义颜色，则循环使用
            const categoryColors = incomeCategories.map((_, index) => pieColors[index % pieColors.length]);
            const categoryBorderColors = categoryColors.map(color => color.replace('0.8', '1'));
            
            new Chart(pieCtx, {
                type: 'pie',
                data: {
                    labels: incomeCategories,
                    datasets: [{
                        data: incomeAmounts,
                        backgroundColor: categoryColors,
                        borderColor: categoryBorderColors,
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'right',
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.raw;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((value / total) * 100).toFixed(1);
                                    return `${label}: ¥${value.toFixed(2)} (${percentage}%)`;
                                }
                            }
                        }
                    }
                }
            });
        }
        
        // 初始化支出按标签分类饼图
        const expenseCategories = JSON.parse(chartDataElement.getAttribute('data-expense-categories'));
        const expenseAmounts = JSON.parse(chartDataElement.getAttribute('data-expense-amounts'));
        if (expenseCategories && expenseCategories.length > 0) {
            const pieCtx = document.getElementById('expenseByCategoryChart').getContext('2d');
            
            // 生成饼图颜色
            const pieColors = [
                'rgba(255, 99, 132, 0.8)',
                'rgba(255, 159, 64, 0.8)',
                'rgba(255, 205, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(153, 102, 255, 0.8)',
                'rgba(201, 203, 207, 0.8)',
                'rgba(199, 199, 199, 0.8)'
            ];
            
            // 为每个类别生成颜色，如果类别数量超过预定义颜色，则循环使用
            const categoryColors = expenseCategories.map((_, index) => pieColors[index % pieColors.length]);
            const categoryBorderColors = categoryColors.map(color => color.replace('0.8', '1'));
            
            new Chart(pieCtx, {
                type: 'pie',
                data: {
                    labels: expenseCategories,
                    datasets: [{
                        data: expenseAmounts,
                        backgroundColor: categoryColors,
                        borderColor: categoryBorderColors,
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'right',
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.raw;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((value / total) * 100).toFixed(1);
                                    return `${label}: ¥${value.toFixed(2)} (${percentage}%)`;
                                }
                            }
                        }
                    }
                }
            });
        }
    
    // 初始化储蓄目标进度条形图
    const goalsData = JSON.parse(chartDataElement.getAttribute('data-goals'));  // 使用后端传来的储蓄目标数据
    if (goalsData && goalsData.length > 0) {
        const barCtx = document.getElementById('goalsProgressChart').getContext('2d');
        
        // 准备数据
        const goalNames = goalsData.map(goal => goal.name.length > 15 ? goal.name.substring(0, 15) + '...' : goal.name);
        const progressValues = goalsData.map(goal => goal.progress_percentage);
        
        new Chart(barCtx, {
            type: 'bar',
            data: {
                labels: goalNames,
                datasets: [{
                    label: '完成进度 (%)',
                    data: progressValues,
                    backgroundColor: 'rgba(54, 162, 235, 0.8)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: '完成百分比 (%)'
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const goal = goalsData[context.dataIndex];
                                return [
                                    '完成进度: ' + context.raw.toFixed(1) + '%',
                                    '当前储蓄: ¥' + goal.current_amount.toFixed(2),
                                    '目标金额: ¥' + goal.target_amount.toFixed(2)
                                ];
                            }
                        }
                    }
                }
            }
        });
    }
});