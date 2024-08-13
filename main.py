import json
import time
import requests
from random import shuffle
# from openai import OpenAI
# ljirwin: import the argparse library for reading in command-line arguments 
import argparse
from src.dataset_handler import Dataset 


def analyze_results(results):
    categories = {}
    for result in results:
        category = result['category']
        categories[category] = categories.get(category, 0) + 1
    
    print("Category distribution:")
    for category, count in categories.items():
        percentage = (count / len(results)) * 100
        print(f"{category}: {percentage:.2f}%")
    
    most_common = max(categories, key=categories.get)
    print(f"Most common category: {most_common}")
    
    avg_answer_length = sum(len(result['answer']) for result in results) / len(results)
    print(f"Average answer length: {avg_answer_length:.2f} characters")

def save_results(results):
    with open("results.json", "w") as f:
        json.dump(results, f)

def main(api_key, model, dataset_url, max_queries, selected_prompt, output_file):
    print("Starting experiment...")
    client = OpenAI(api_key=API_KEY)
    dataset_handler = DatasetHandler(dataset_url=dataset_url, max_queries=max_queries)
    questions = dataset_handler.download_dataset()
    results = dataset_hanlder.process_dataset(questions, client)
    analyze_results(results)
    save_results(results)
    print("Experiment complete.")

if __name__ == "__main__":
    # ljirwin: Added arguments to replace the hard-coded experiment variables. 
    parser = argparse.ArgumentParser()
    # ljirwin: Argument for api key 
    parser.add_argument('--api_key', type=str, required=True, help="The OpenAI API key for your experiment")
    # ljirwin: Argument for model
    parser.add_argument('--model', type=str, required=True, default="gpt-3.5-turbo", help="The OpenAI model for your experiment")
    # ljirwin: Argument for the dataset URL
    parser.add_argument('--dataset_url', type=str, default="https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json", help="Dataset URL (Must be in JSON format)")
    # ljirwin: Argument for the max number of queries
    parser.add_argument('--max_queries', type=int, default=10000,)
    # ljirwin: Argument for the prompt variation to use
    parser.add_argument('--prompt_variation', type=int, default=1,)
    # ljirwin: Argument for the output file name (to be configured for the overwriting issue)
    parser.add_argument('--output_file', type=str, required=True, default="results.json", help="Name of the output file")

    args = parser.parse_args()
    # ljirwin: Testing to see that argsparser has been implemented
    # print(f"API key check: {args.api_key}")
    PROMPT_VARIATIONS = [
        "Categorize and answer the following question. Respond in JSON format with 'category' and 'answer' fields:",
        "Please provide a category and answer for this question. Use JSON format with 'category' and 'answer' keys:",
        "Analyze and respond to the following question. Return a JSON with 'category' for the question type and 'answer' for your response:",
    ]
    selected_prompt = PROMPT_VARIATIONS[args.prompt_variation]

    main(
        api_key=args.api_key,
        model=args.model,
        dataset_url=args.dataset_url,
        max_queries=args.max_queries,
        selected_prompt=selected_prompt,
        output_file=args.output_file
    )