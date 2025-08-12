# AI_platform_CrewAI   

## debate folder  
Context    
This process is to discuss an idea *It is good to work at CBA in Australia for a long time* among debators who support or argue against this idea and it is up to a judge to decide who wins and provide reasons.The outcomes for these three agents could be found in https://github.com/ruihukuang/AI_platform_CrewAI/tree/main/debate/output.    
This process is sequential.  
- The first task is related to a debator to propose this idea.  
- The second task is related to a debator to express opposite idea.  
- The third task is related to a judge to decide which idea is better.      

## financial_researcher folder  
Context  
This process is to write a report for a company based on serper APIs with google search APIs. The google web search could make sure a report is created based on the latest info from internet rather than just knowledge bases on AI models. The target company is Commonwealth Bank of Australia. The report for this could be found in https://github.com/ruihukuang/AI_platform_CrewAI/blob/main/financial_researcher/output_cba/report.md.  
This process is sequential. Tasks are executed one after the other.   
- The first task is related to a researcher to research the company, news and potential for a company based on serper APIs with google search APIs.    
- The second task is related to a analyst to analyze the research findings and create a comprehensive report on this company.  

## stock_picker folder    
Context    
This process is to find the top trending companies in the latest news in a sector, do detailed analysis, pick the best company for investment and send a push notification to my phone. The target sector is banks in Australia. The output could be found in https://github.com/ruihukuang/AI_platform_CrewAI/blob/main/stock_picker/output/decision.md. This process uses a file to preserve insights and learnings ,building knowledge over time in the long term memory, use RAG to store recent interactions and outcomes in the short term memory and use RAG to store entity info about people, places, concepts during tasks in the entity memory.   
This process is hierarchical. There is dedicated manager agent that oversees task execution, planning, and validation, delegating subtasks to worker agents. 3 worker agents run their tasks in order.    
- The first agent *Trending_company_finder* is to find the top trending companies in the news in a sector by searching the latest news using serper APIs with google search APIs.    
- The second agent *financial_researcher* is to do detailed analysis given the a list of trending companies from the first agent.   
- The third agent *stock_picker* is to analyze the research findings from the second agent, pick the best company for investment and send a push notification to an app in pusher on my phone with the decision and 1 sentence rationale.  

## coder folder   
Context  
This process is to use python code to do some calculations. The outcome could be found in https://github.com/ruihukuang/AI_platform_CrewAI/blob/main/coder/output/code_and_output.txt. This process uses docker images to run in a local container in the docker desktop. The screenshot below is about docker images.   
<img width="2993" height="836" alt="image" src="https://github.com/user-attachments/assets/9763dec0-7946-40ce-bbbf-e0d6d19ed5f8" />  







