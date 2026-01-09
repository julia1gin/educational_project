import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ============================================
# ГЕНЕРАЦИЯ ТЕСТОВЫХ ДАННЫХ
# ============================================

def generate_test_data():
    """Создание тестовых данных для анализа"""
    np.random.seed(42)
    students = [f'Ученик_{i}' for i in range(1, 26)]
    n_questions = 15
    
    # Результаты теста (0 или 1)
    results_data = {'Ученик': students}
    for i in range(1, n_questions + 1):
        # Разная сложность: первые 5 - легкие, средние 5 - средние, последние 5 - сложные
        if i <= 5:
            prob = 0.85  # 85% правильных
        elif i <= 10:
            prob = 0.65  # 65% правильных
        else:
            prob = 0.45  # 45% правильных
        
        results_data[f'Задание_{i}'] = np.random.choice([0, 1], size=len(students), p=[1-prob, prob])
    
    results_df = pd.DataFrame(results_data)
    
    # Информация о заданиях
    topics = ['Квадратные уравнения'] * 3 + ['Теорема Пифагора'] * 3 + \
             ['Тригонометрия'] * 3 + ['Логарифмы'] * 3 + ['Производная'] * 3
    
    difficulty = ['Легко'] * 5 + ['Средне'] * 5 + ['Сложно'] * 5
    
    test_info_df = pd.DataFrame({
        'Задание': [f'Задание_{i}' for i in range(1, n_questions + 1)],
        'Тема': topics,
        'Макс_балл': [1] * n_questions,
        'Сложность': difficulty
    })
    
    print("✅ Тестовые данные сгенерированы")
    return results_df, test_info_df

# ============================================
# АНАЛИЗ РЕЗУЛЬТАТОВ
# ============================================

def analyze_test_results(results_df, test_info_df):
    """Полный анализ результатов тестирования"""
    question_cols = [col for col in results_df.columns if col.startswith('Задание_')]
    
    # Общие баллы учеников
    results_df['Общий_балл'] = results_df[question_cols].sum(axis=1)
    results_df['Процент'] = (results_df['Общий_балл'] / len(question_cols) * 100).round(1)
    
    # Статистика по заданиям
    question_stats = []
    for col in question_cols:
        correct = results_df[col].sum()
        total = len(results_df)
        percentage = (correct / total * 100).round(1)
        topic = test_info_df[test_info_df['Задание'] == col]['Тема'].values[0]
        difficulty = test_info_df[test_info_df['Задание'] == col]['Сложность'].values[0]
        
        question_stats.append({
            'Задание': col,
            'Тема': topic,
            'Сложность': difficulty,
            'Правильных_ответов': correct,
            'Процент_правильных': percentage,
            'Проблемное': 'Да' if percentage < 60 else 'Нет'
        })
    
    question_stats_df = pd.DataFrame(question_stats)
    
    # Статистика по темам
    topic_stats = question_stats_df.groupby('Тема').agg({
        'Процент_правильных': 'mean'
    }).round(1).reset_index()
    topic_stats['Проблемная_тема'] = topic_stats['Процент_правильных'].apply(lambda x: 'Да' if x < 60 else 'Нет')
    
    return results_df, question_stats_df, topic_stats

# ============================================
# ВИЗУАЛИЗАЦИЯ
# ============================================

def create_analysis_dashboard(results_df, question_stats_df, topic_stats):
    """Создание дашборда с визуализацией"""
    fig = plt.figure(figsize=(20, 12))
    fig.suptitle('ДАШБОРД АНАЛИЗА ТЕСТИРОВАНИЯ', fontsize=24, fontweight='bold', y=0.98)
    
    # 1. Успеваемость по заданиям (столбчатая)
    ax1 = plt.subplot(2, 2, 1)
    sns.barplot(x='Задание', y='Процент_правильных', data=question_stats_df, palette='viridis', ax=ax1)
    ax1.axhline(60, color='red', linestyle='--', label='Порог 60%')
    ax1.set_title('Успеваемость по заданиям', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Процент правильных (%)')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
    ax1.legend()
    
    # 2. Успеваемость по темам (столбчатая)
    ax2 = plt.subplot(2, 2, 2)
    sns.barplot(x='Тема', y='Процент_правильных', data=topic_stats, palette='Set2', ax=ax2)
    ax2.axhline(60, color='red', linestyle='--', label='Порог 60%')
    ax2.set_title('Успеваемость по темам', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Средний процент правильных (%)')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
    ax2.legend()
    
    # 3. Распределение баллов учеников (гистограмма)
    ax3 = plt.subplot(2, 2, 3)
    sns.histplot(results_df['Процент'], kde=True, color='skyblue', ax=ax3)
    ax3.set_title('Распределение процентов правильных ответов', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Процент правильных (%)')
    
    # 4. Топ проблемных заданий (горизонтальная)
    ax4 = plt.subplot(2, 2, 4)
    problem_questions = question_stats_df[question_stats_df['Процент_правильных'] < 60].sort_values('Процент_правильных')
    sns.barplot(x='Процент_правильных', y='Задание', data=problem_questions, palette='YlOrRd', ax=ax4)
    ax4.set_title('Проблемные задания (менее 60%)', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Процент правильных (%)')
    
    plt.tight_layout()
    plt.savefig('test_analysis_dashboard.png', dpi=300, bbox_inches='tight')
    print("✅ Дашборд сохранён в test_analysis_dashboard.png")
    plt.show()

# ============================================
# СОЗДАНИЕ ОТЧЁТА
# ============================================

def create_report(results_df, question_stats_df, topic_stats, report_filename='test_report.txt'):
    """Генерация текстового отчёта с рекомендациями"""
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("ОТЧЁТ ПО АНАЛИЗУ ТЕСТИРОВАНИЯ\n")
        f.write("=" * 80 + "\n")
        f.write(f"Дата отчёта: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n")
        
        f.write("1. ОБЩАЯ СТАТИСТИКА\n")
        f.write("-" * 80 + "\n")
        f.write(f"Всего учеников: {len(results_df)}\n")
        f.write(f"Всего заданий: {len(question_stats_df)}\n")
        f.write(f"Средний процент правильных по классу: {results_df['Процент'].mean():.1f}%\n")
        f.write(f"Медиана: {results_df['Процент'].median():.1f}%\n")
        f.write(f"Минимальный результат: {results_df['Процент'].min():.1f}%\n")
        f.write(f"Максимальный результат: {results_df['Процент'].max():.1f}%\n\n")
        
        f.write("2. СТАТИСТИКА ПО ЗАДАНИЯМ\n")
        f.write("-" * 80 + "\n")
        for _, row in question_stats_df.iterrows():
            f.write(f"{row['Задание']} ({row['Тема']}, {row['Сложность']}): {row['Процент_правильных']:.1f}% правильных\n")
        
        f.write("\n3. ПРОБЛЕМНЫЕ ЗАДАНИЯ (<60% правильных)\n")
        f.write("-" * 80 + "\n")
        problem_questions = question_stats_df[question_stats_df['Процент_правильных'] < 60]
        if len(problem_questions) > 0:
            for _, row in problem_questions.iterrows():
                f.write(f"{row['Задание']} ({row['Тема']}): {row['Процент_правильных']:.1f}%\n")
        else:
            f.write("Нет проблемных заданий\n")
        
        f.write("\n4. СТАТИСТИКА ПО ТЕМАМ\n")
        f.write("-" * 80 + "\n")
        for _, row in topic_stats.iterrows():
            f.write(f"{row['Тема']}: {row['Процент_правильных']:.1f}% правильных ({row['Проблемная_тема']})\n")
        
        f.write("\n5. УЧЕНИКИ С НИЗКИМИ РЕЗУЛЬТАТАМИ (<50% правильных)\n")
        f.write("-" * 80 + "\n")
        struggling = results_df[results_df['Процент'] < 50].sort_values('Процент')
        if len(struggling) > 0:
            for _, row in struggling.iterrows():
                f.write(f"{row['Ученик']}: {row['Процент']:.1f}% ({row['Общий_балл']} баллов)\n")
        else:
            f.write("Все ученики справились\n")
        
        f.write("\n6. РЕКОМЕНДАЦИИ\n")
        f.write("-" * 80 + "\n")
        
        problem_topics = topic_stats[topic_stats['Процент_правильных'] < 60]
        if len(problem_topics) > 0:
            f.write("📚 Провести дополнительные занятия по темам:\n")
            for _, row in problem_topics.iterrows():
                f.write(f"   - {row['Тема']}\n")
        
        if len(struggling) > 0:
            f.write(f"\n👥 Организовать консультации для {len(struggling)} учеников\n")
        
        if results_df['Процент'].mean() < 60:
            f.write("\n⚠️ Средний результат ниже ожидаемого. Рекомендуется:\n")
            f.write("   - Пересмотреть методику\n")
            f.write("   - Уделить внимание практическим заданиям\n")
            f.write("   - Провести разбор ошибок\n")
        
        f.write("\n" + "=" * 80 + "\n")
    
    print(f"✅ Отчёт сохранён в {report_filename}")

# ============================================
# СОХРАНЕНИЕ В EXCEL
# ============================================

def save_to_excel(results_df, question_stats_df, topic_stats, filename='test_analysis.xlsx'):
    """Сохранение в Excel"""
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        results_df.to_excel(writer, sheet_name='Результаты учеников', index=False)
        question_stats_df.to_excel(writer, sheet_name='Статистика по заданиям', index=False)
        topic_stats.to_excel(writer, sheet_name='Статистика по темам', index=False)
    
    print(f"✅ Результаты сохранены в {filename}")

# ============================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================

def main():
    """Главная функция анализа тестирования"""
    print("\n" + "=" * 80)
    print("СИСТЕМА АНАЛИЗА РЕЗУЛЬТАТОВ ТЕСТИРОВАНИЯ")
    print("=" * 80 + "\n")
    
    # Генерация данных
    print("📊 Генерация тестовых данных...")
    results_df, test_info_df = generate_test_data()
    
    # Анализ
    print("🔍 Анализ результатов...")
    results_df, question_stats_df, topic_stats = analyze_test_results(results_df, test_info_df)
    
    # Вывод краткой статистики
    print(f"\n✅ Анализ завершён!")
    print(f"   Средний процент правильных: {results_df['Процент'].mean():.1f}%")
    print(f"   Лучший результат: {results_df['Процент'].max():.1f}%")
    print(f"   Худший результат: {results_df['Процент'].min():.1f}%")
    
    # Визуализация
    print("\n📈 Создание визуализаций...")
    create_analysis_dashboard(results_df, question_stats_df, topic_stats)
    
    # Отчёт
    print("📝 Формирование отчёта...")
    create_report(results_df, question_stats_df, topic_stats)
    
    # Сохранение в Excel
    print("💾 Сохранение результатов в Excel...")
    save_to_excel(results_df, question_stats_df, topic_stats)
    
    print("\n" + "=" * 80)
    print("Анализ завершён! Все файлы созданы.")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()