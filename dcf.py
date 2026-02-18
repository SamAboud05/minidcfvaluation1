import pandas as pd

def load_inputs(path="inputs.xlsx"):
    df = pd.read_excel(path, header=None)
    inputs = {row[0]: row[1] for _, row in df.iterrows()}
    return inputs

def project_fcfs(rev_year1, growth, margin, tax, years=5):
    revenues = []
    fcfs = []
    rev = rev_year1

    for _ in range(years):
        rev = rev * (1 + growth)
        revenues.append(rev)

        ebit = rev * margin
        nopat = ebit * (1 - tax)
        fcfs.append(nopat)

    return revenues, fcfs

def compute_terminal_value(last_fcf, wacc, g):
    return last_fcf * (1 + g) / (wacc - g)

def discount_cash_flows(fcfs, terminal_value, wacc):
    discounted_fcfs = [
        fcfs[i] / ((1 + wacc) ** (i + 1)) for i in range(len(fcfs))
    ]
    discounted_terminal = terminal_value / ((1 + wacc) ** len(fcfs))
    return discounted_fcfs, discounted_terminal

def main():
    inputs = load_inputs("inputs.xlsx")
    print(inputs.keys())

    rev_y1      = inputs["Revenue (Year 1)"]
    growth      = inputs["Revenue Growth Rate"]
    margin      = inputs["Operating Margin"]
    tax         = inputs["Tax Rate"]
    wacc        = inputs["WACC"]
    g_terminal  = inputs["Terminal Growth Rate"]
    shares      = inputs["Shares Outstanding"]

    revenues, fcfs = project_fcfs(rev_y1, growth, margin, tax)
    terminal_value = compute_terminal_value(fcfs[-1], wacc, g_terminal)
    discounted_fcfs, discounted_terminal = discount_cash_flows(fcfs, terminal_value, wacc)

    enterprise_value = sum(discounted_fcfs) + discounted_terminal
    intrinsic_value = enterprise_value / shares

    print("----- Mini DCF Valuation -----")
    for i, (rev, fcf, d_fcf) in enumerate(zip(revenues, fcfs, discounted_fcfs), start=1):
        print(f"Year {i}: Revenue = {rev:,.0f}, FCF = {fcf:,.0f}, Discounted FCF = {d_fcf:,.0f}")

    print(f"\nTerminal Value (undiscounted): {terminal_value:,.0f}")
    print(f"Discounted Terminal Value: {discounted_terminal:,.0f}")
    print(f"\nEnterprise Value: {enterprise_value:,.0f}")
    print(f"Intrinsic Value per Share: ${intrinsic_value:,.2f}")
if __name__ == "__main__":
    main()