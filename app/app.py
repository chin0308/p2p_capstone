import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Project - NexCore P2P",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

C = {
    "blue_dark"  : "#1F5B99",
    "red"        : "#C0392B",
    "amber"      : "#E8A04A",
    "teal"       : "#2E9E8F",
    "gray"       : "#7F8C8D",
    "header_bg"  : "#4BACC6",
    "header_txt" : "#1A4F72",
    "page_bg"    : "#F7F9FB",
    "card_bg"    : "#FFFFFF",
    "border"     : "#D6E4F0",
    "d1": "#2B5F9E", "d2": "#8B1A1A", "d3": "#E67E22",
    "d4": "#27AE60", "d5": "#1ABC9C", "d6": "#9B59B6", "d7": "#F39C12",
}
DONUT_COLORS = ["#1ABC9C","#2B5F9E","#E67E22","#27AE60","#8B1A1A","#9B59B6","#F39C12"]
BAR_COLORS   = ["#9B59B6","#E8A04A","#4BACC6","#2E9E8F","#1F5B99"]
st.markdown(f"""
<style>
  .stApp {{ background:{C["page_bg"]}; }}
  .block-container {{ padding:1.2rem 1.8rem 2rem; }}
  [data-testid="stSidebar"] {{ background:#EBF5FB; border-right:1px solid {C["border"]}; }}

  .kpi-row {{ display:flex; gap:10px; margin-bottom:18px; }}
  .kpi-card {{
      flex:1; border-radius:4px; padding:14px 16px 12px;
      display:flex; flex-direction:column; align-items:center; justify-content:center;
  }}
  .kpi-label  {{ font-size:10.5px; font-weight:700; letter-spacing:.6px; color:rgba(255,255,255,.85);
                 text-transform:uppercase; margin-bottom:6px; text-align:center; }}
  .kpi-value  {{ font-size:32px; font-weight:800; color:#fff; line-height:1; }}
  .kpi-sub    {{ font-size:10px; color:rgba(255,255,255,.7); margin-top:4px; }}

  .sec-hdr {{ background:{C["header_bg"]}; color:#fff; font-size:12.5px; font-weight:700;
              letter-spacing:.4px; padding:5px 10px; border-radius:3px;
              margin-bottom:10px; margin-top:6px; }}

  .chart-card  {{ background:{C["card_bg"]}; border:1px solid {C["border"]};
                  border-radius:6px; padding:14px 16px 10px; }}
  .chart-title {{ font-size:12px; font-weight:700; color:{C["header_txt"]};
                  margin-bottom:4px; padding-bottom:4px; border-bottom:2px solid {C["header_bg"]}; }}

  .page-title  {{ font-size:19px; font-weight:800; color:#1A2D45; margin-bottom:2px; }}
  .page-sub    {{ font-size:11.5px; color:{C["header_txt"]}; margin-bottom:14px; font-weight:600; }}
  #MainMenu, footer, header {{ visibility:hidden; }}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(path):
    df = pd.read_csv(path, parse_dates=["Order_Date","Delivery_Date","GR_Date","Invoice_Date"])
    df["Month"]     = df["Order_Date"].dt.to_period("M").astype(str)
    df["On_Time"]   = df["Delay_Days"].apply(lambda x: "On-Time" if x==0 else "Delayed")
    df["Delay_Band"]= pd.cut(df["Delay_Days"], bins=[-1,0,5,10,20,999],
        labels=["None (0d)","Low (1-5d)","Medium (6-10d)","High (11-20d)","Severe (>20d)"])
    return df

DATA = Path(__file__).parent.parent / "data" / "p2p_dataset.csv"

with st.sidebar:
    st.markdown("### 📦 NexCore P2P")
    st.markdown("---")
    up = st.file_uploader("Upload CSV", type=["csv"])
    if up:
        df_raw = pd.read_csv(up, parse_dates=["Order_Date","Delivery_Date","GR_Date","Invoice_Date"])
        df_raw["Month"]     = df_raw["Order_Date"].dt.to_period("M").astype(str)
        df_raw["On_Time"]   = df_raw["Delay_Days"].apply(lambda x: "On-Time" if x==0 else "Delayed")
        df_raw["Delay_Band"]= pd.cut(df_raw["Delay_Days"],bins=[-1,0,5,10,20,999],
            labels=["None (0d)","Low (1-5d)","Medium (6-10d)","High (11-20d)","Severe (>20d)"])
    else:
        df_raw = load_data(str(DATA))

    st.markdown("**Filters**")
    vendors  = st.multiselect("Vendor",         sorted(df_raw["Vendor_Name"].unique()),    default=sorted(df_raw["Vendor_Name"].unique()))
    statuses = st.multiselect("Payment Status", sorted(df_raw["Payment_Status"].unique()), default=sorted(df_raw["Payment_Status"].unique()))
    plants   = st.multiselect("Plant",          sorted(df_raw["Plant"].unique()),          default=sorted(df_raw["Plant"].unique()))
    dates    = st.date_input("Date Range",
        [df_raw["Order_Date"].min().date(), df_raw["Order_Date"].max().date()])
    st.markdown("---")
    st.caption("© 2024 NexCore Capstone")

df = df_raw.copy()
if vendors:  df = df[df["Vendor_Name"].isin(vendors)]
if statuses: df = df[df["Payment_Status"].isin(statuses)]
if plants:   df = df[df["Plant"].isin(plants)]
if len(dates)==2:
    df = df[(df["Order_Date"].dt.date>=dates[0])&(df["Order_Date"].dt.date<=dates[1])]

N = len(df)
pending_n = int((df["Payment_Status"]=="Pending").sum())
overdue_n = int((df["Payment_Status"]=="Overdue").sum())
paid_n = int((df["Payment_Status"]=="Paid").sum())
delay_rate = int(round((df["Delay_Days"]>0).mean()*100)) if N else 0
total_spend = df["Total_Amount"].sum()
avg_delay = df["Delay_Days"].mean() if N else 0

st.markdown('<div class="page-title">Project – NexCore P2P Analytics</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="page-sub">▼ Procurement Information &nbsp;|&nbsp; '
    f'Total Spend: <b>₹{total_spend/1e7:.2f} Cr</b> &nbsp;|&nbsp; '
    f'Avg Delay: <b>{avg_delay:.1f} days</b></div>',
    unsafe_allow_html=True)

st.markdown('<div class="sec-hdr">▼ Procurement Overview</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="kpi-row">
  <div class="kpi-card" style="background:{C['blue_dark']}">
    <div class="kpi-label">Total POs</div>
    <div class="kpi-value">{N}</div>
    <div class="kpi-sub">Purchase Orders</div>
  </div>
  <div class="kpi-card" style="background:{C['red']}">
    <div class="kpi-label">Pending</div>
    <div class="kpi-value">{pending_n}</div>
    <div class="kpi-sub">Awaiting Payment</div>
  </div>
  <div class="kpi-card" style="background:{C['amber']}">
    <div class="kpi-label">Overdue</div>
    <div class="kpi-value">{overdue_n}</div>
    <div class="kpi-sub">Past Due Date</div>
  </div>
  <div class="kpi-card" style="background:{C['teal']}">
    <div class="kpi-label">Paid</div>
    <div class="kpi-value">{paid_n}</div>
    <div class="kpi-sub">Invoices Cleared</div>
  </div>
  <div class="kpi-card" style="background:{C['gray']}">
    <div class="kpi-label">Delay Rate</div>
    <div class="kpi-value">{delay_rate} %</div>
    <div class="kpi-sub">Orders Delayed</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="sec-hdr">▼ Breakdown Analysis</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

def make_donut(labels, values, colors, hover):
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.50, direction="clockwise",
        marker=dict(colors=colors, line=dict(color="#fff",width=1.5)),
        textinfo="label+percent",
        textfont=dict(size=9),
        hovertemplate=hover,
        pull=[0.03]*len(labels),
    ))
    fig.update_layout(
        margin=dict(t=8,b=8,l=4,r=4), showlegend=False, height=220,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig

with c1:
    vd = df.groupby("Vendor_Name")["PO_ID"].count().sort_values(ascending=False).head(6)
    labels = [n.split()[0] for n in vd.index]
    st.markdown('<div class="chart-card"><div class="chart-title">Vendor PO Distribution</div>', unsafe_allow_html=True)
    st.plotly_chart(
        make_donut(labels, vd.values.tolist(), DONUT_COLORS[:len(vd)],
            "<b>%{label}</b><br>PO Count: <b>%{value}</b><br>Share: <b>%{percent}</b>"
            "<br><i>Hover = vendor info</i><extra></extra>"),
        use_container_width=True, config={"displayModeBar":False})
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    db = df["Delay_Band"].value_counts()
    band_colors = ["#27AE60","#E67E22","#F39C12","#C0392B","#8B1A1A"][:len(db)]
    st.markdown('<div class="chart-card"><div class="chart-title">Delivery Delay Breakdown</div>', unsafe_allow_html=True)
    st.plotly_chart(
        make_donut(db.index.tolist(), db.values.tolist(), band_colors,
            "<b>%{label}</b><br>Orders: <b>%{value}</b><br>% of Total: <b>%{percent}</b>"
            "<br><i>Delay band distribution</i><extra></extra>"),
        use_container_width=True, config={"displayModeBar":False})
    st.markdown("</div>", unsafe_allow_html=True)

with c3:
    pc = df["Payment_Status"].value_counts()
    pay_col_map = {"Paid":C["teal"],"Pending":C["amber"],"Overdue":C["red"]}
    pcols = [pay_col_map.get(s, C["gray"]) for s in pc.index]
    st.markdown('<div class="chart-card"><div class="chart-title">Payment Status Breakdown</div>', unsafe_allow_html=True)
    st.plotly_chart(
        make_donut(pc.index.tolist(), pc.values.tolist(), pcols,
            "<b>%{label}</b><br>Invoices: <b>%{value}</b><br>Share: <b>%{percent}</b>"
            "<br><i>Payment action status</i><extra></extra>"),
        use_container_width=True, config={"displayModeBar":False})
    st.markdown("</div>", unsafe_allow_html=True)


st.markdown('<div class="sec-hdr">▼ Category Breakdowns</div>', unsafe_allow_html=True)
c4, c5 = st.columns(2)

# Bar 1 – Spend by Material (top 5)
with c4:
    ms = df.groupby("Material")["Total_Amount"].sum().sort_values(ascending=False).head(5)
    fig_b1 = go.Figure()
    for i, (mat, val) in enumerate(ms.items()):
        fig_b1.add_trace(go.Bar(
            y=[mat], x=[val], orientation="h",
            marker_color=BAR_COLORS[i % len(BAR_COLORS)],
            name=mat,
            text=[f"₹{val/1e5:.1f}L"],
            textposition="inside", insidetextanchor="end",
            textfont=dict(color="white", size=10),
            hovertemplate=(
                f"<b>{mat}</b><br>"
                "Total Spend: <b>₹%{{x:,.0f}}</b><br>"
                "<i>SAP Table: EKPO (material item)</i>"
                "<extra></extra>"
            ),
        ))
    fig_b1.update_layout(
        height=195, margin=dict(t=5,b=5,l=0,r=10),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, tickfont=dict(size=10), autorange="reversed"),
        bargap=0.25,
    )
    st.markdown('<div class="chart-card"><div class="chart-title">Spend by Material (Top 5) — INR</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_b1, use_container_width=True, config={"displayModeBar":False})
    st.markdown("</div>", unsafe_allow_html=True)

with c5:
    def lead_band(row):
        d = (pd.to_datetime(row["Delivery_Date"]) - pd.to_datetime(row["Order_Date"])).days
        if d <= 7:   return "Short-Term (≤7d)"
        elif d <= 14: return "Medium-Term (8-14d)"
        else:         return "Long-Term (>14d)"

    df["Lead_Band"] = df.apply(lead_band, axis=1)
    lb = df["Lead_Band"].value_counts().reindex(
        ["Short-Term (≤7d)","Medium-Term (8-14d)","Long-Term (>14d)"]).fillna(0).astype(int)
    lb_colors = [C["teal"], C["amber"], C["red"]]

    fig_b2 = go.Figure()
    for i, (band, cnt) in enumerate(lb.items()):
        pct = cnt/N*100 if N else 0
        fig_b2.add_trace(go.Bar(
            y=[band], x=[int(cnt)], orientation="h",
            marker_color=lb_colors[i], name=band,
            text=[str(int(cnt))],
            textposition="inside", insidetextanchor="end",
            textfont=dict(color="white", size=11),
            hovertemplate=(
                f"<b>{band}</b><br>"
                "Purchase Orders: <b>%{x}</b><br>"
                f"Share of All POs: <b>{pct:.0f}%</b><br>"
                "<i>Delivery lead-time category</i>"
                "<extra></extra>"
            ),
        ))
    fig_b2.update_layout(
        height=195, margin=dict(t=5,b=5,l=0,r=10),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, tickfont=dict(size=10), autorange="reversed"),
        bargap=0.30,
    )
    st.markdown('<div class="chart-card"><div class="chart-title">PO Delivery Timeframe Breakdown</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_b2, use_container_width=True, config={"displayModeBar":False})
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="sec-hdr">▼ Monthly Spend Trend</div>', unsafe_allow_html=True)

monthly = (df.groupby("Month")
             .agg(Spend=("Total_Amount","sum"), POs=("PO_ID","count"))
             .reset_index())
monthly["MA3"] = monthly["Spend"].rolling(3, min_periods=1).mean()

fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(
    x=monthly["Month"], y=monthly["Spend"],
    mode="lines+markers", fill="tozeroy",
    fillcolor="rgba(75,172,198,0.13)",
    line=dict(color=C["header_bg"], width=2.5),
    marker=dict(color=C["blue_dark"], size=7, line=dict(color="#fff",width=1.5)),
    name="Monthly Spend",
    customdata=monthly[["POs","MA3"]].values,
    hovertemplate=(
        "<b>Month: %{x}</b><br>"
        "Total Spend: <b>₹%{y:,.0f}</b><br>"
        "PO Count: <b>%{customdata[0]}</b><br>"
        "3-Month Avg: <b>₹%{customdata[1]:,.0f}</b><br>"
        "<i>Source: SAP EKKO (order header)</i>"
        "<extra></extra>"
    ),
))
fig_trend.add_trace(go.Scatter(
    x=monthly["Month"], y=monthly["MA3"],
    mode="lines", line=dict(color=C["red"],width=1.5,dash="dash"),
    name="3-Month Avg",
    hovertemplate=(
        "<b>%{x}</b><br>"
        "3-Month Moving Avg: <b>₹%{y:,.0f}</b>"
        "<extra></extra>"
    ),
))
fig_trend.update_layout(
    height=215, margin=dict(t=10,b=10,l=10,r=10),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False, tickfont=dict(size=9.5),
               title=dict(text="Month", font=dict(size=10))),
    yaxis=dict(gridcolor="#E8EFF5", tickfont=dict(size=9.5),
               title=dict(text="Spend (INR)", font=dict(size=10))),
    legend=dict(orientation="h", yanchor="bottom", y=1.02,
                xanchor="right", x=1, font=dict(size=9.5)),
    hovermode="x unified",
)
st.markdown('<div class="chart-card"><div class="chart-title">Monthly Procurement Spend (INR) — dashed = 3-month moving average</div>', unsafe_allow_html=True)
st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar":False})
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="sec-hdr">▼ Vendor Scorecard &amp; Data Explorer</div>', unsafe_allow_html=True)
tab_v, tab_d = st.tabs(["Vendor Scorecard", "Raw Data"])

with tab_v:
    vs = (df.groupby("Vendor_Name")
            .agg(Total_Spend=("Total_Amount","sum"),
                 PO_Count=("PO_ID","count"),
                 Avg_Delay=("Delay_Days","mean"),
                 Paid=("Payment_Status", lambda x:(x=="Paid").sum()),
                 Overdue=("Payment_Status", lambda x:(x=="Overdue").sum()))
            .reset_index()
            .sort_values("Total_Spend", ascending=False))
    vs["Risk"]     = vs["Avg_Delay"].apply(lambda x:"Low" if x<=5 else("Medium" if x<=10 else"High"))
    vs["Spend"]    = vs["Total_Spend"].map("₹{:,.0f}".format)
    vs["Avg Delay"]= vs["Avg_Delay"].map("{:.1f}d".format)
    st.dataframe(
        vs[["Vendor_Name","Spend","PO_Count","Avg Delay","Paid","Overdue","Risk"]]
          .rename(columns={"Vendor_Name":"Vendor","PO_Count":"POs"}),
        use_container_width=True, hide_index=True)

with tab_d:
    s = st.text_input("Search vendor / material / PO ID")
    d2 = df.copy()
    if s:
        m = (d2["Vendor_Name"].str.contains(s,case=False,na=False)|
             d2["Material"].str.contains(s,case=False,na=False)|
             d2["PO_ID"].str.contains(s,case=False,na=False))
        d2 = d2[m]
    st.caption(f"{len(d2)} records")
    st.dataframe(d2[["PO_ID","Vendor_Name","Material","Plant","Order_Date",
                      "Delivery_Date","Quantity","Total_Amount","Delay_Days",
                      "Payment_Status","Payment_Terms"]].reset_index(drop=True),
                 use_container_width=True, height=320)
    st.download_button("Download CSV", d2.to_csv(index=False).encode(),
                       "p2p_filtered.csv","text/csv")
st.markdown(f"""
<div style="text-align:center;padding:16px 0 4px;font-size:10px;
            color:{C['gray']};border-top:1px solid {C['border']};margin-top:20px;">
  NexCore Manufacturing Pvt Ltd &nbsp;·&nbsp; SAP P2P Analytics &nbsp;·&nbsp;
  Streamlit + Plotly &nbsp;·&nbsp; Capstone 2024
</div>
""", unsafe_allow_html=True)