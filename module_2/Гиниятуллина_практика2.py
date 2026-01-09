import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Настройки стиля
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 100

# ============================================
# ГЕНЕРАЦИЯ ТЕСТОВЫХ ДАННЫХ
# ============================================

def generate_test_data():
    """Создание тестовых данных для дашборда"""
    np.random.seed(42)
    n_students = 25
    
    students = [f'Ученик_{i}' for i in range(1, n_students + 1)]
    subjects = ['Математика', 'Теорема Пифагора', 'Русский', 'Физика', 'Информатика']
    
    data = {'Ученик': students}
    for subject in subjects:
        data[subject] = np.random.randint(2, 6, n_students)
    
    df = pd.DataFrame(data)
    df['Средний_балл'] = df[subjects].mean(axis=1).round(2)
    
    # Данные по четвертям для динамики
    quarters_data = pd.DataFrame({
        'Четверть': ['1 четв.', '2 четв.', '3 четв.', '4 четв.'],
        'Средний_балл': [3.9, 4.0, 4.2, 4.3]
    })
    
    return df, quarters_data

# ============================================
# СОЗДАНИЕ ДАШБОРДА
# ============================================

def create_dashboard(df, quarters_data):
    """Создание дашборда с графиками"""
    fig = plt.figure(figsize=(20, 12))
    fig.suptitle('ДАШБОРД УСПЕВАЕМОСТИ КЛАССА', fontsize=24, fontweight='bold', y=0.98)
    
    subjects = [col for col in df.columns if col not in ['Ученик', 'Средний_балл']]
    
    # 1. Средние баллы по предметам (столбчатая диаграмма)
    ax1 = plt.subplot(3, 3, 1)
    subject_means = df[subjects].mean().sort_values(ascending=False)
    colors = plt.cm.viridis(np.linspace(0, 1, len(subjects)))
    bars = ax1.bar(range(len(subjects)), subject_means.values, color=colors, edgecolor='black')
    ax1.set_xticks(range(len(subjects)))
    ax1.set_xticklabels(subject_means.index, rotation=45, ha='right')
    ax1.set_ylabel('Средний балл', fontsize=11, fontweight='bold')
    ax1.set_title('Средние баллы по предметам', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, 5)
    ax1.grid(axis='y', alpha=0.3)
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                 f'{height:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # 2. Распределение оценок (круговая диаграмма)
    ax2 = plt.subplot(3, 3, 2)
    all_grades = pd.concat([df[subject] for subject in subjects])
    grade_counts = all_grades.value_counts().sort_index()
    colors_pie = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db', '#9b59b6']
    ax2.pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%', 
            colors=colors_pie[:len(grade_counts)], startangle=90, 
            shadow=True, explode=[0.05] * len(grade_counts))
    ax2.set_title('Распределение оценок по классу', fontsize=12, fontweight='bold')
    
    # 3. Топ-10 учеников (горизонтальная столбчатая)
    ax3 = plt.subplot(3, 3, 3)
    top_students = df.sort_values('Средний_балл', ascending=False).head(10)
    sns.barplot(x='Средний_балл', y='Ученик', data=top_students, palette='viridis', ax=ax3)
    ax3.set_title('Топ-10 учеников', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Средний балл', fontsize=11, fontweight='bold')
    ax3.set_ylabel('')
    for i, v in enumerate(top_students['Средний_балл']):
        ax3.text(v + 0.05, i, f'{v:.2f}', va='center', fontweight='bold')
    
    # 4. Тепловая карта оценок
    ax4 = plt.subplot(3, 3, 4)
    heatmap_data = df.set_index('Ученик')[subjects]
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='d', 
                linewidths=0.5, cbar_kws={'label': 'Балл'}, ax=ax4)
    ax4.set_title('Тепловая карта оценок', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Предмет', fontsize=11, fontweight='bold')
    ax4.set_ylabel('Ученик', fontsize=11, fontweight='bold')
    
    # 5. Динамика успеваемости по четвертям (линейный график)
    ax5 = plt.subplot(3, 3, 5)
    ax5.plot(quarters_data['Четверть'], quarters_data['Средний_балл'], 
             marker='o', linewidth=3, markersize=12, color='#3498db')
    ax5.set_ylabel('Средний балл класса', fontsize=11, fontweight='bold')
    ax5.set_title('Динамика успеваемости по четвертям', fontsize=12, fontweight='bold')
    ax5.grid(True, alpha=0.3)
    ax5.set_ylim(3.5, 4.5)
    for i, row in quarters_data.iterrows():
        ax5.text(i, row['Средний_балл'] + 0.05, f"{row['Средний_балл']:.1f}",
                 ha='center', fontweight='bold', fontsize=10)
    
    # 6. Box plot для сравнения предметов
    ax6 = plt.subplot(3, 3, 6)
    df_melted = df[subjects].melt(var_name='Предмет', value_name='Балл')
    sns.boxplot(x='Предмет', y='Балл', data=df_melted, palette='Set2', ax=ax6)
    ax6.set_title('Разброс оценок по предметам', fontsize=12, fontweight='bold')
    ax6.set_xlabel('Предмет', fontsize=11, fontweight='bold')
    ax6.set_ylabel('Балл', fontsize=11, fontweight='bold')
    ax6.set_xticklabels(ax6.get_xticklabels(), rotation=45, ha='right')
    ax6.grid(axis='y', alpha=0.3)
    
    # 7. Статистический блок
    ax7 = plt.subplot(3, 3, 7)
    ax7.axis('off')
    
    stats = {
        'Всего учеников': len(df),
        'Средний балл': df['Средний_балл'].mean().round(2),
        'Медиана': df['Средний_балл'].median().round(2),
        'Отличников (≥4.5)': len(df[df['Средний_балл'] >= 4.5]),
        'Хорошистов (≥3.5)': len(df[(df['Средний_балл'] >= 3.5) & (df['Средний_балл'] < 4.5)]),
        'Троечников (<3.5)': len(df[df['Средний_балл'] < 3.5])
    }
    
    best_subject = subject_means.idxmax()
    worst_subject = subject_means.idxmin()
    
    stats_text = f"""
{'='*40}
   СТАТИСТИКА КЛАССА
{'='*40}

Всего учеников: {stats['Всего учеников']}

Средний балл: {stats['Средний балл']:.2f}
Медиана: {stats['Медиана']:.2f}

РАСПРЕДЕЛЕНИЕ:
  Отличников: {stats['Отличников (≥4.5)']}
  Хорошистов: {stats['Хорошистов (≥3.5)']}
  Троечников: {stats['Троечников (<3.5)']}

ПРЕДМЕТЫ:
  Лучший: {best_subject}
           ({subject_means[best_subject]:.2f})
  Сложный: {worst_subject}
           ({subject_means[worst_subject]:.2f})

Дата: {datetime.now().strftime('%d.%m.%Y')}
{'='*40}
"""
    
    ax7.text(0.05, 0.95, stats_text, transform=ax7.transAxes,
             fontsize=11, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('dashboard.png', dpi=300, bbox_inches='tight')
    print("✅ Дашборд сохранён в dashboard.png")
    plt.show()

# ============================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================

def main():
    """Главная функция создания дашборда"""
    print("\n" + "=" * 80)
    print("СОЗДАНИЕ ДАШБОРДА УСПЕВАЕМОСТИ")
    print("=" * 80 + "\n")
    
    # Генерация данных
    print("📊 Генерация тестовых данных...")
    df, quarters_data = generate_test_data()
    
    # Создание дашборда
    print("📈 Создание дашборда...")
    create_dashboard(df, quarters_data)
    
    print("\n✅ Дашборд завершён!")

if __name__ == "__main__":
    main()