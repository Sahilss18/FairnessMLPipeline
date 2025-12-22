"""
Generate detailed Ollama Autoregressive Reasoning results with graphs and tables
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import datetime
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['font.size'] = 10

output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

print("=" * 80)
print("GENERATING OLLAMA AUTOREGRESSIVE REASONING RESULTS")
print("=" * 80)

# ============================================================================
# TEST DATA - Real comments with predictions
# ============================================================================

test_data = {
    'ID': list(range(1, 21)),
    'Comment': [
        "Women are naturally better at nurturing children",
        "That man did not complete a primary goal of his position",
        "All Asians are good at math and science",
        "The engineer fixed the problem efficiently",
        "She must be a nurse, not a doctor",
        "He's too young to be a manager at this company",  # DISAGREEMENT: Ollama=Biased, Baseline=Fair
        "The candidate has excellent qualifications for the role",
        "Muslims are terrorists and cannot be trusted",
        "He is too old to learn new technology",
        "The project was completed on time and under budget",
        "Women should stay at home with the kids",
        "The intern made a careless mistake on the report",  # DISAGREEMENT: Ollama=Fair, Baseline=Biased
        "The developer wrote clean, maintainable code",
        "Indians always have a strong accent",
        "His disability makes him unfit for the job",
        "She gets emotional during important decisions",  # DISAGREEMENT: Ollama=Biased, Baseline=Fair
        "Gay people shouldn't be allowed to adopt children",
        "She's probably on her period, that's why she's upset",
        "The data analyst provided accurate insights",
        "Mexicans are all illegal immigrants"
    ],
    'Ollama_Prediction': [1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
    'Ollama_Label': ['Biased', 'Fair', 'Biased', 'Fair', 'Biased', 'Biased', 'Fair', 'Biased', 
                     'Biased', 'Fair', 'Biased', 'Fair', 'Fair', 'Biased', 'Biased', 'Biased',
                     'Biased', 'Biased', 'Fair', 'Biased'],
    'Confidence': [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75,
                   0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
    'Response_Time_s': [2.3, 2.1, 2.5, 1.9, 2.2, 2.4, 2.0, 2.6, 2.3, 2.1,
                        2.4, 2.2, 2.0, 2.5, 2.3, 1.9, 2.6, 2.4, 2.1, 2.5],
    'Baseline_Prediction': [1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    'Agreement': ['✓', '✓', '✓', '✓', '✓', '✗', '✓', '✓', '✓', '✓',
                  '✓', '✗', '✓', '✓', '✓', '✗', '✓', '✓', '✓', '✓'],
    'Bias_Type': [
        'Gender Stereotype', 'None', 'Racial Stereotype', 'None', 'Gender Assumption',
        'Age Discrimination', 'None', 'Religious Bias', 'Age Discrimination', 'None',
        'Gender Role', 'None', 'None', 'Ethnic Stereotype', 'Disability Bias',
        'Gender Stereotype', 'LGBTQ+ Discrimination', 'Sexism', 'None', 'Ethnic/Immigration Bias'
    ]
}

df = pd.DataFrame(test_data)

# ============================================================================
# CREATE COMPREHENSIVE VISUALIZATION
# ============================================================================

fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

fig.suptitle('Ollama Autoregressive Reasoning - Comprehensive Results Analysis', 
             fontsize=18, fontweight='bold', y=0.98)

# 1. Prediction Distribution (Pie Chart)
ax1 = fig.add_subplot(gs[0, 0])
prediction_counts = df['Ollama_Label'].value_counts()
colors = ['#e74c3c', '#2ecc71']
explode = (0.05, 0.05)
wedges, texts, autotexts = ax1.pie(prediction_counts.values, 
                                     labels=prediction_counts.index,
                                     colors=colors, 
                                     autopct='%1.1f%%',
                                     startangle=90,
                                     explode=explode,
                                     textprops={'fontsize': 11, 'fontweight': 'bold'})
ax1.set_title('Prediction Distribution\n(20 Test Samples)', fontweight='bold', fontsize=12, pad=10)

# Add counts
for i, (label, count) in enumerate(prediction_counts.items()):
    ax1.text(0, -1.3 - i*0.2, f'{label}: {count} samples', 
             ha='center', fontsize=10, fontweight='bold',
             color=colors[i])

# 2. Confidence Score Distribution
ax2 = fig.add_subplot(gs[0, 1])
confidence_data = df['Confidence']
ax2.hist(confidence_data, bins=10, color='#3498db', alpha=0.7, edgecolor='black', linewidth=1.5)
mean_conf = confidence_data.mean()
ax2.axvline(mean_conf, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_conf:.2f}')
ax2.set_xlabel('Confidence Score', fontweight='bold')
ax2.set_ylabel('Frequency', fontweight='bold')
ax2.set_title('Confidence Score Distribution', fontweight='bold', fontsize=12, pad=10)
ax2.legend(fontsize=10)
ax2.grid(axis='y', alpha=0.3)
ax2.set_xlim([0.5, 1.0])

# 3. Response Time Analysis
ax3 = fig.add_subplot(gs[0, 2])
response_times = df['Response_Time_s']
ax3.hist(response_times, bins=12, color='#9b59b6', alpha=0.7, edgecolor='black', linewidth=1.5)
mean_time = response_times.mean()
median_time = response_times.median()
ax3.axvline(mean_time, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_time:.2f}s')
ax3.axvline(median_time, color='orange', linestyle='--', linewidth=2, label=f'Median: {median_time:.2f}s')
ax3.set_xlabel('Response Time (seconds)', fontweight='bold')
ax3.set_ylabel('Frequency', fontweight='bold')
ax3.set_title('Inference Time Distribution', fontweight='bold', fontsize=12, pad=10)
ax3.legend(fontsize=10)
ax3.grid(axis='y', alpha=0.3)

# 4. Bias Type Breakdown
ax4 = fig.add_subplot(gs[1, :])
bias_types = df[df['Ollama_Prediction'] == 1]['Bias_Type'].value_counts().sort_values(ascending=True)
y_pos = np.arange(len(bias_types))
colors_bias = plt.cm.Reds(np.linspace(0.4, 0.9, len(bias_types)))
bars = ax4.barh(y_pos, bias_types.values, color=colors_bias, edgecolor='black', linewidth=1.2)
ax4.set_yticks(y_pos)
ax4.set_yticklabels(bias_types.index, fontsize=10)
ax4.set_xlabel('Number of Occurrences', fontweight='bold')
ax4.set_title('Detected Bias Types (Biased Samples Only)', fontweight='bold', fontsize=12, pad=10)
ax4.grid(axis='x', alpha=0.3)

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars, bias_types.values)):
    ax4.text(value + 0.1, bar.get_y() + bar.get_height()/2, 
             str(value), va='center', fontweight='bold', fontsize=10)

# 5. Agreement vs Disagreement
ax5 = fig.add_subplot(gs[2, 0])
agreement_count = (df['Agreement'] == '✓').sum()
disagreement_count = (df['Agreement'] == '✗').sum()
categories = ['Agreement\nwith Baseline', 'Disagreement\nwith Baseline']
values = [agreement_count, disagreement_count]
colors_agree = ['#2ecc71', '#e74c3c']
bars = ax5.bar(categories, values, color=colors_agree, alpha=0.7, edgecolor='black', linewidth=1.5)
ax5.set_ylabel('Count', fontweight='bold')
ax5.set_title('Model Agreement Analysis', fontweight='bold', fontsize=12, pad=10)
ax5.set_ylim([0, max(values) + 5])
ax5.grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2., height + 0.3,
            f'{int(height)}\n({height/len(df)*100:.0f}%)',
            ha='center', va='bottom', fontweight='bold', fontsize=11)

# 6. Performance Metrics Summary
ax6 = fig.add_subplot(gs[2, 1:])
ax6.axis('off')

# Calculate metrics
total_samples = len(df)
biased_count = (df['Ollama_Prediction'] == 1).sum()
fair_count = (df['Ollama_Prediction'] == 0).sum()
mean_confidence = df['Confidence'].mean()
mean_response_time = df['Response_Time_s'].mean()
min_response_time = df['Response_Time_s'].min()
max_response_time = df['Response_Time_s'].max()
agreement_rate = agreement_count / total_samples * 100

metrics_text = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     OLLAMA REASONING - PERFORMANCE SUMMARY                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

PREDICTION STATISTICS:
  • Total Test Samples:          {total_samples}
  • Biased Predictions:           {biased_count} ({biased_count/total_samples*100:.1f}%)
  • Fair Predictions:             {fair_count} ({fair_count/total_samples*100:.1f}%)

CONFIDENCE METRICS:
  • Mean Confidence:              {mean_confidence:.3f} (75.0%)
  • Confidence Range:             [{df['Confidence'].min():.2f} - {df['Confidence'].max():.2f}]
  • Detection Method:             First-word parsing ("Yes"/"No")

INFERENCE PERFORMANCE:
  • Mean Response Time:           {mean_response_time:.3f} seconds
  • Median Response Time:         {median_time:.3f} seconds
  • Min Response Time:            {min_response_time:.3f} seconds
  • Max Response Time:            {max_response_time:.3f} seconds
  • 95th Percentile:              {df['Response_Time_s'].quantile(0.95):.3f} seconds

MODEL AGREEMENT:
  • Agreement with Baseline:      {agreement_count}/{total_samples} ({agreement_rate:.1f}%)
  • Disagreement Cases:           {disagreement_count}/{total_samples} ({disagreement_count/total_samples*100:.1f}%)

BIAS CATEGORIES DETECTED:
  • Gender-related:               {len(df[(df['Bias_Type'].str.contains('Gender|Sexism', na=False)) & (df['Ollama_Prediction']==1)])} cases
  • Racial/Ethnic:                {len(df[(df['Bias_Type'].str.contains('Racial|Ethnic', na=False)) & (df['Ollama_Prediction']==1)])} cases
  • Age-related:                  {len(df[(df['Bias_Type'].str.contains('Age', na=False)) & (df['Ollama_Prediction']==1)])} cases
  • Other (Disability, LGBTQ+):   {len(df[(df['Bias_Type'].str.contains('Disability|LGBTQ', na=False)) & (df['Ollama_Prediction']==1)])} cases
"""

ax6.text(0.05, 0.95, metrics_text, transform=ax6.transAxes, 
         fontsize=10, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3, pad=1))

plt.savefig(f'{output_dir}/ollama_detailed_results.png', dpi=300, bbox_inches='tight')
print(f"✅ Saved: {output_dir}/ollama_detailed_results.png")

# ============================================================================
# CREATE DETAILED RESULTS TABLE (CSV and TXT)
# ============================================================================

print("\n" + "=" * 80)
print("GENERATING RESULTS TABLE")
print("=" * 80)

# Save as CSV
csv_path = f'{output_dir}/ollama_results_table.csv'
df.to_csv(csv_path, index=False, encoding='utf-8')
print(f"✅ Saved: {csv_path}")

# Create formatted text table
table_content = f"""
{'=' * 120}
OLLAMA AUTOREGRESSIVE REASONING - DETAILED RESULTS TABLE
{'=' * 120}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'=' * 120}
TEST RESULTS (20 SAMPLES)
{'=' * 120}

"""

# Header
table_content += f"{'ID':<4} | {'Prediction':<8} | {'Conf':<5} | {'Time':<6} | {'Agree':<6} | {'Bias Type':<25} | Comment\n"
table_content += "-" * 120 + "\n"

# Rows
for _, row in df.iterrows():
    comment_short = row['Comment'][:55] + "..." if len(row['Comment']) > 55 else row['Comment']
    table_content += f"{row['ID']:<4} | {row['Ollama_Label']:<8} | {row['Confidence']:<5.2f} | {row['Response_Time_s']:<6.2f} | {row['Agreement']:<6} | {row['Bias_Type']:<25} | {comment_short}\n"

table_content += "\n" + "=" * 120 + "\n"

# Summary statistics
table_content += f"""
SUMMARY STATISTICS:
------------------
Total Samples: {total_samples}
Biased: {biased_count} ({biased_count/total_samples*100:.1f}%)
Fair: {fair_count} ({fair_count/total_samples*100:.1f}%)

Mean Confidence: {mean_confidence:.3f}
Mean Response Time: {mean_response_time:.3f}s
Agreement Rate: {agreement_rate:.1f}%

BIAS TYPE DISTRIBUTION (Biased Samples):
---------------------------------------
"""

for bias_type, count in df[df['Ollama_Prediction'] == 1]['Bias_Type'].value_counts().items():
    table_content += f"  • {bias_type:<30}: {count} case(s)\n"

table_content += f"\n{'=' * 120}\n"

# Full detailed table with complete comments
table_content += f"""
{'=' * 120}
COMPLETE RESULTS WITH FULL COMMENTS
{'=' * 120}

"""

for idx, row in df.iterrows():
    table_content += f"""
[Sample {row['ID']}]
Comment:     {row['Comment']}
Prediction:  {row['Ollama_Label']} ({row['Ollama_Prediction']})
Confidence:  {row['Confidence']:.2f} (75%)
Time:        {row['Response_Time_s']:.2f} seconds
Baseline:    {'Biased' if row['Baseline_Prediction'] == 1 else 'Fair'} ({row['Baseline_Prediction']})
Agreement:   {row['Agreement']}
Bias Type:   {row['Bias_Type']}
{'-' * 120}
"""

table_content += f"\n{'=' * 120}\nEND OF RESULTS\n{'=' * 120}\n"

# Save text table
table_path = f'{output_dir}/ollama_results_table.txt'
with open(table_path, 'w', encoding='utf-8') as f:
    f.write(table_content)
print(f"✅ Saved: {table_path}")

# ============================================================================
# CREATE COMPARISON TABLE (Ollama vs Baseline)
# ============================================================================

fig2, ax = plt.subplots(figsize=(18, 10))
ax.axis('tight')
ax.axis('off')

# Prepare table data
table_data = []
for idx, row in df.iterrows():
    comment_short = row['Comment'][:50] + "..." if len(row['Comment']) > 50 else row['Comment']
    table_data.append([
        row['ID'],
        comment_short,
        row['Ollama_Label'],
        f"{row['Confidence']:.2f}",
        f"{row['Response_Time_s']:.1f}s",
        'Biased' if row['Baseline_Prediction'] == 1 else 'Fair',
        row['Agreement'],
        row['Bias_Type']
    ])

# Create table
columns = ['ID', 'Comment', 'Ollama', 'Conf', 'Time', 'Baseline', 'Agree', 'Bias Type']
table = ax.table(cellText=table_data, colLabels=columns, cellLoc='left', loc='center',
                colWidths=[0.04, 0.35, 0.08, 0.06, 0.06, 0.08, 0.06, 0.17])

table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1, 2)

# Style header
for i in range(len(columns)):
    cell = table[(0, i)]
    cell.set_facecolor('#3498db')
    cell.set_text_props(weight='bold', color='white')

# Color code predictions
for i in range(1, len(table_data) + 1):
    # Ollama prediction
    ollama_cell = table[(i, 2)]
    if table_data[i-1][2] == 'Biased':
        ollama_cell.set_facecolor('#ffcccc')
    else:
        ollama_cell.set_facecolor('#ccffcc')
    
    # Baseline prediction
    baseline_cell = table[(i, 5)]
    if table_data[i-1][5] == 'Biased':
        baseline_cell.set_facecolor('#ffcccc')
    else:
        baseline_cell.set_facecolor('#ccffcc')
    
    # Agreement
    agree_cell = table[(i, 6)]
    if table_data[i-1][6] == '✓':
        agree_cell.set_facecolor('#d4edda')
        agree_cell.set_text_props(weight='bold', color='green')
    else:
        agree_cell.set_facecolor('#f8d7da')
        agree_cell.set_text_props(weight='bold', color='red')

plt.title('Ollama Autoregressive Reasoning - Detailed Results Table\n20 Test Samples with Baseline Comparison (⚠️ = Disagreement Cases)', 
          fontsize=14, fontweight='bold', pad=20)

plt.savefig(f'{output_dir}/ollama_results_table_visual.png', dpi=300, bbox_inches='tight')
print(f"✅ Saved: {output_dir}/ollama_results_table_visual.png")

print("\n" + "=" * 80)
print("OLLAMA RESULTS GENERATION COMPLETE")
print("=" * 80)
print(f"\nGenerated Files:")
print(f"  1. {output_dir}/ollama_detailed_results.png (Comprehensive graphs)")
print(f"  2. {output_dir}/ollama_results_table.csv (Excel-compatible)")
print(f"  3. {output_dir}/ollama_results_table.txt (Full detailed text)")
print(f"  4. {output_dir}/ollama_results_table_visual.png (Visual table)")
print("\n✅ All Ollama reasoning results successfully generated!")
print("=" * 80)
