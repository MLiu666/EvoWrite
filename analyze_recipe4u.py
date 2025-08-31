#!/usr/bin/env python3
"""
RECIPE4U Dataset Analysis Script
Analyzes the structure, content, and patterns in the RECIPE4U dataset
for EFL writing education research.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
import json

# Set up matplotlib for Chinese font support
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_and_explore_dataset(file_path):
    """Load the RECIPE4U dataset and perform initial exploration."""
    print("Loading RECIPE4U dataset...")
    
    try:
        df = pd.read_csv(file_path)
        print(f"Dataset loaded successfully!")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

def basic_statistics(df):
    """Generate basic statistics about the dataset."""
    print("\n" + "="*50)
    print("BASIC DATASET STATISTICS")
    print("="*50)
    
    # Basic info
    print(f"Total number of interactions: {len(df)}")
    print(f"Number of unique students: {df['student_id'].nunique()}")
    print(f"Number of unique courses: {df['course'].nunique()}")
    print(f"Course distribution: {df['course'].value_counts().to_dict()}")
    
    # Temporal analysis
    print(f"Week range: {df['week'].min()} to {df['week'].max()}")
    print(f"Session range: {df['session'].min()} to {df['session'].max()}")
    
    # Rating analysis
    print(f"Rating distribution: {df['rating'].value_counts().sort_index().to_dict()}")
    print(f"Average rating: {df['rating'].mean():.2f}")
    
    # Intent analysis
    print(f"Number of unique intents: {df['intent_final'].nunique()}")
    print(f"Top 5 intents: {df['intent_final'].value_counts().head().to_dict()}")
    
    # Boolean flags
    print(f"Quiz questions: {df['is_quiz'].sum()} ({df['is_quiz'].mean()*100:.1f}%)")
    print(f"Essay edits: {df['is_essay_edited'].sum()} ({df['is_essay_edited'].mean()*100:.1f}%)")

def analyze_text_content(df):
    """Analyze the text content in user utterances and ChatGPT responses."""
    print("\n" + "="*50)
    print("TEXT CONTENT ANALYSIS")
    print("="*50)
    
    # User utterance analysis
    user_texts = df['user'].dropna()
    user_lengths = user_texts.str.len()
    user_word_counts = user_texts.str.split().str.len()
    
    print(f"User utterances:")
    print(f"  Average length (characters): {user_lengths.mean():.1f}")
    print(f"  Average word count: {user_word_counts.mean():.1f}")
    print(f"  Median length (characters): {user_lengths.median():.1f}")
    
    # ChatGPT response analysis
    chatgpt_texts = df['chatgpt_after'].dropna()
    chatgpt_lengths = chatgpt_texts.str.len()
    chatgpt_word_counts = chatgpt_texts.str.split().str.len()
    
    print(f"ChatGPT responses:")
    print(f"  Average length (characters): {chatgpt_lengths.mean():.1f}")
    print(f"  Average word count: {chatgpt_word_counts.mean():.1f}")
    print(f"  Median length (characters): {chatgpt_lengths.median():.1f}")
    
    return user_lengths, chatgpt_lengths, user_word_counts, chatgpt_word_counts

def analyze_learning_patterns(df):
    """Analyze learning patterns across time and students."""
    print("\n" + "="*50)
    print("LEARNING PATTERN ANALYSIS")
    print("="*50)
    
    # Student engagement patterns
    student_interactions = df.groupby('student_id').size()
    print(f"Average interactions per student: {student_interactions.mean():.1f}")
    print(f"Median interactions per student: {student_interactions.median():.1f}")
    print(f"Most active student: {student_interactions.max()} interactions")
    print(f"Least active student: {student_interactions.min()} interactions")
    
    # Weekly progression
    weekly_stats = df.groupby('week').agg({
        'rating': 'mean',
        'is_quiz': 'mean',
        'is_essay_edited': 'mean',
        'student_id': 'nunique'
    }).round(3)
    
    print(f"\nWeekly progression:")
    print(weekly_stats)
    
    # Course-specific patterns
    course_stats = df.groupby('course').agg({
        'rating': 'mean',
        'is_quiz': 'mean',
        'is_essay_edited': 'mean',
        'student_id': 'nunique'
    }).round(3)
    
    print(f"\nCourse-specific patterns:")
    print(course_stats)
    
    return student_interactions, weekly_stats, course_stats

def create_visualizations(df, user_lengths, chatgpt_lengths, student_interactions, weekly_stats):
    """Create visualizations of the dataset patterns."""
    print("\n" + "="*50)
    print("CREATING VISUALIZATIONS")
    print("="*50)
    
    # Set up the plotting style
    plt.style.use('default')
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('RECIPE4U Dataset Analysis', fontsize=16, fontweight='bold')
    
    # 1. Rating distribution
    axes[0, 0].hist(df['rating'], bins=5, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('Rating Distribution')
    axes[0, 0].set_xlabel('Rating (1-5)')
    axes[0, 0].set_ylabel('Frequency')
    
    # 2. Course distribution
    course_counts = df['course'].value_counts()
    axes[0, 1].pie(course_counts.values, labels=course_counts.index, autopct='%1.1f%%')
    axes[0, 1].set_title('Course Distribution')
    
    # 3. Intent distribution (top 10)
    intent_counts = df['intent_final'].value_counts().head(10)
    axes[0, 2].barh(range(len(intent_counts)), intent_counts.values)
    axes[0, 2].set_yticks(range(len(intent_counts)))
    axes[0, 2].set_yticklabels(intent_counts.index, fontsize=8)
    axes[0, 2].set_title('Top 10 Intent Categories')
    axes[0, 2].set_xlabel('Frequency')
    
    # 4. Text length comparison
    axes[1, 0].boxplot([user_lengths.dropna(), chatgpt_lengths.dropna()], 
                       labels=['User', 'ChatGPT'])
    axes[1, 0].set_title('Text Length Comparison')
    axes[1, 0].set_ylabel('Character Count')
    
    # 5. Student interaction distribution
    axes[1, 1].hist(student_interactions, bins=20, alpha=0.7, color='lightgreen', edgecolor='black')
    axes[1, 1].set_title('Student Interaction Distribution')
    axes[1, 1].set_xlabel('Number of Interactions')
    axes[1, 1].set_ylabel('Number of Students')
    
    # 6. Weekly rating trends
    axes[1, 2].plot(weekly_stats.index, weekly_stats['rating'], marker='o', linewidth=2)
    axes[1, 2].set_title('Weekly Rating Trends')
    axes[1, 2].set_xlabel('Week')
    axes[1, 2].set_ylabel('Average Rating')
    axes[1, 2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/recipe4u_analysis.png', dpi=300, bbox_inches='tight')
    print("Visualizations saved to: /home/ubuntu/recipe4u_analysis.png")
    
    return fig

def analyze_intent_patterns(df):
    """Analyze intent patterns and their relationship with other variables."""
    print("\n" + "="*50)
    print("INTENT PATTERN ANALYSIS")
    print("="*50)
    
    # Intent-rating correlation
    intent_rating = df.groupby('intent_final')['rating'].agg(['mean', 'count']).round(2)
    intent_rating = intent_rating[intent_rating['count'] >= 10]  # Filter for intents with at least 10 occurrences
    intent_rating = intent_rating.sort_values('mean', ascending=False)
    
    print("Intent categories with highest average ratings (min 10 occurrences):")
    print(intent_rating.head(10))
    
    # Intent-course relationship
    intent_course = pd.crosstab(df['intent_final'], df['course'], normalize='columns') * 100
    print(f"\nIntent distribution by course (%):")
    print(intent_course.round(1))
    
    return intent_rating, intent_course

def extract_sample_interactions(df, n_samples=5):
    """Extract sample interactions for qualitative analysis."""
    print("\n" + "="*50)
    print("SAMPLE INTERACTIONS")
    print("="*50)
    
    # Get high-rated interactions
    high_rated = df[df['rating'] >= 4].sample(n_samples, random_state=42)
    
    print("Sample high-rated interactions:")
    for i, (_, row) in enumerate(high_rated.iterrows(), 1):
        print(f"\n--- Sample {i} (Rating: {row['rating']}, Intent: {row['intent_final']}) ---")
        print(f"Student: {row['user'][:200]}...")
        print(f"ChatGPT: {row['chatgpt_after'][:200]}...")
    
    return high_rated

def generate_summary_report(df):
    """Generate a comprehensive summary report."""
    print("\n" + "="*50)
    print("SUMMARY REPORT")
    print("="*50)
    
    report = {
        "dataset_overview": {
            "total_interactions": len(df),
            "unique_students": df['student_id'].nunique(),
            "unique_courses": df['course'].nunique(),
            "week_range": f"{df['week'].min()}-{df['week'].max()}",
            "average_rating": round(df['rating'].mean(), 2)
        },
        "engagement_metrics": {
            "avg_interactions_per_student": round(df.groupby('student_id').size().mean(), 1),
            "quiz_question_rate": round(df['is_quiz'].mean() * 100, 1),
            "essay_edit_rate": round(df['is_essay_edited'].mean() * 100, 1)
        },
        "content_analysis": {
            "avg_user_text_length": round(df['user'].str.len().mean(), 1),
            "avg_chatgpt_text_length": round(df['chatgpt_after'].str.len().mean(), 1),
            "top_intents": df['intent_final'].value_counts().head(5).to_dict()
        }
    }
    
    # Save report as JSON
    with open('/home/ubuntu/recipe4u_summary.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("Summary report saved to: /home/ubuntu/recipe4u_summary.json")
    print(json.dumps(report, indent=2))
    
    return report

def main():
    """Main analysis function."""
    print("RECIPE4U Dataset Analysis")
    print("=" * 50)
    
    # Load dataset
    df = load_and_explore_dataset('/home/ubuntu/RECIPE4U.csv')
    if df is None:
        return
    
    # Perform analyses
    basic_statistics(df)
    user_lengths, chatgpt_lengths, user_word_counts, chatgpt_word_counts = analyze_text_content(df)
    student_interactions, weekly_stats, course_stats = analyze_learning_patterns(df)
    intent_rating, intent_course = analyze_intent_patterns(df)
    sample_interactions = extract_sample_interactions(df)
    
    # Create visualizations
    fig = create_visualizations(df, user_lengths, chatgpt_lengths, student_interactions, weekly_stats)
    
    # Generate summary report
    report = generate_summary_report(df)
    
    print("\n" + "="*50)
    print("ANALYSIS COMPLETE")
    print("="*50)
    print("Files generated:")
    print("- /home/ubuntu/recipe4u_analysis.png (visualizations)")
    print("- /home/ubuntu/recipe4u_summary.json (summary report)")

if __name__ == "__main__":
    main()

