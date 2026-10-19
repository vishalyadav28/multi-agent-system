from src.pipelines.pipeline import run_research_pipeline

# output = web_search.invoke({"query": "latest news on AI today"})

# output = scrape_url.invoke({"url": "https://www.reddit.com/r/artificial/"})

# print(output)

topic = "The impact of AI on the job market in 2026"

result = run_research_pipeline(topic)


print(result)


