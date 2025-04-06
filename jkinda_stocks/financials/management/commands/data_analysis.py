from langchain.llms import OpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
import pandas as pd

# Define the LLM
llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)

# Define a tool for analyzing a company's balance sheet
def balance_sheet_analysis_tool(file_path: str) -> str:
    try:
        df = pd.read_csv(file_path)
        
        # Ensure data is sorted by period (assuming a 'Period' column exists)
        df = df.sort_values(by=['Period'])
        
        # Extract key financial metrics
        metrics = [
            'Total Assets', 'Total Liabilities', 'Total Equity', 'Current Assets', 'Current Liabilities',
            'Net Income', 'Revenue', 'Retained Earnings', 'Operating Cash Flow', 'Total Debt', 'EBIT', 'EBITDA',
            'Market Capitalization', 'Free Cash Flow', 'Gross Profit', 'Operating Income'
        ]
        
        # Compute financial ratios for each period
        df['Debt-to-Equity Ratio'] = df['Total Liabilities'] / df['Total Equity']
        df['Current Ratio'] = df['Current Assets'] / df['Current Liabilities']
        df['Return on Assets'] = df['Net Income'] / df['Total Assets']
        df['Return on Equity'] = df['Net Income'] / df['Total Equity']
        df['Profit Margin'] = df['Net Income'] / df['Revenue']
        df['Operating Cash Flow Ratio'] = df['Operating Cash Flow'] / df['Current Liabilities']
        df['Debt Ratio'] = df['Total Debt'] / df['Total Assets']
        df['EBITDA Margin'] = df['EBITDA'] / df['Revenue']
        df['Interest Coverage Ratio'] = df['EBIT'] / df['Total Debt']
        df['Price-to-Earnings Ratio'] = df['Market Capitalization'] / df['Net Income']
        df['Free Cash Flow Yield'] = df['Free Cash Flow'] / df['Market Capitalization']
        df['Gross Margin'] = df['Gross Profit'] / df['Revenue']
        df['Operating Margin'] = df['Operating Income'] / df['Revenue']
        
        # Compute period-over-period changes
        df_changes = df[['Period'] + metrics].copy()
        df_changes.set_index('Period', inplace=True)
        df_changes = df_changes.pct_change().round(2) * 100  # Convert to percentage changes
        df_changes = df_changes.fillna('N/A')  # Handle NaN values
        
        summary = "Balance Sheet Analysis with Periodic Changes:\n"
        summary += df_changes.to_string()
        
        # Graham's Intelligent Investor Model
        graham_criteria = {
            'Current Ratio': 2.0,
            'Debt-to-Equity Ratio': 1.0,
            'Return on Equity': 0.15,
            'Price-to-Earnings Ratio': 15,
            'Interest Coverage Ratio': 5.0,
            'Profit Margin': 0.10,
            'Free Cash Flow Yield': 0.05
        }
        
        fits_criteria = []
        fails_criteria = []
        
        for metric, threshold in graham_criteria.items():
            if metric in df.columns:
                latest_value = df[metric].iloc[-1]
                if latest_value >= threshold:
                    fits_criteria.append(f"{metric}: {latest_value} (Meets requirement: {threshold})")
                else:
                    fails_criteria.append(f"{metric}: {latest_value} (Below requirement: {threshold})")
        
        graham_summary = "\nGraham’s Intelligent Investor Analysis:\n\nFits Criteria:\n" + "\n".join(fits_criteria) + "\n\nFails Criteria:\n" + "\n".join(fails_criteria)
        
        return summary + graham_summary
    except Exception as e:
        return f"Error processing balance sheet: {str(e)}"

# Define tools available to the agent
tools = [
    Tool(
        name="BalanceSheetAnalyzer",
        func=balance_sheet_analysis_tool,
        description="Analyzes a company's balance sheet from a CSV file, extracts key financial insights, tracks period-over-period changes, and compares with Graham’s Intelligent Investor model."
    )
]

# Initialize memory for conversational context
memory = ConversationBufferMemory(memory_key="chat_history")

# Initialize the agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

def analyze_balance_sheet(file_path: str):
    """Analyzes the given company's balance sheet and provides insights for stock buyers, including trends over time, industry comparisons, and Graham’s model evaluation."""
    prompt = (
        f"Analyze the balance sheet in {file_path} and extract key financial insights relevant to stock buyers."
        " Focus on liquidity, profitability, debt levels, valuation, financial stability, period-over-period changes, industry benchmark comparisons, and Graham’s Intelligent Investor criteria."
    )
    return agent.run(prompt)

# Example usage
if __name__ == "__main__":
    file_path = "balance_sheet.csv"  # Replace with your actual CSV file path
    print(analyze_balance_sheet(file_path))
