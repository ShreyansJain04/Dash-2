import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Load and process your data
df = pd.read_excel('C:\\Users\\Vidhi Shah\\Downloads\\Trans-base-priority-wise-with-priority_2.xlsx')

# Get unique states from the data

states = sorted(df['State'].dropna().unique())
print("Available states:", states)

# State-specific business intelligence
state_insights = {
    'MH': {
        'full_name': 'Maharashtra',
        'key_cities': 'Mumbai, Pune, Nagpur',
        'market_focus': 'Urban housing boom, Infrastructure projects',
        'challenges': 'High competition, Price sensitivity',
        'opportunities': 'Metro expansion, Smart city initiatives'
    },
    'APTS': {
        'full_name': 'Andhra Pradesh & Telangana',
        'key_cities': 'Hyderabad, Vijayawada, Visakhapatnam',
        'market_focus': 'Government infrastructure, Industrial growth',
        'challenges': 'Bid cancellations, Project delays',
        'opportunities': '10-18% demand growth expected, Capital city development'
    },
    'TN': {
        'full_name': 'Tamil Nadu',
        'key_cities': 'Chennai, Coimbatore, Madurai',
        'market_focus': 'Industrial construction, Port development',
        'challenges': 'Limestone levy impact, Brand loyalty',
        'opportunities': 'Industrial corridors, Port modernization'
    },
    'KA': {
        'full_name': 'Karnataka',
        'key_cities': 'Bangalore, Mysore, Hubli',
        'market_focus': 'IT parks, Residential growth',
        'challenges': 'Competition from neighboring states',
        'opportunities': 'Tech hub expansion, Aerospace sector'
    },
    'WB': {
        'full_name': 'West Bengal',
        'key_cities': 'Kolkata, Asansol, Durgapur',
        'market_focus': 'Port infrastructure, Industrial revival',
        'challenges': 'Economic slowdown impact',
        'opportunities': 'Eastern freight corridor, Port expansion'
    }
}

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Color scheme for priorities
priority_colors = {
    'P1': '#28a745',  # Green
    'P2': '#17a2b8',  # Blue  
    'P3': '#ffc107',  # Yellow
    'P4': '#dc3545'   # Red
}

app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("🏭 State-wise Customer Priority Analytics", 
                   className="text-center mb-4",
                   style={'color': '#2c3e50', 'fontWeight': 'bold'}),
            html.P("Comprehensive cement industry customer intelligence across Indian states", 
                   className="text-center text-muted"),
            html.Hr()
        ])
    ]),
    
    # State Selection
    dbc.Row([
        dbc.Col([
            html.Label("Select State:", style={'fontWeight': 'bold', 'fontSize': '16px'}),
            dcc.Dropdown(
                id='state-selector',
                options=[
                    {'label': f"{state} ({state_insights.get(state, {}).get('full_name', state)})", 
                     'value': state} 
                    for state in states
                ],
                value=states[0] if states else 'MH',
                clearable=False,
                style={'fontSize': '14px'}
            )
        ], width=6),
        dbc.Col([
            html.Div(id='state-overview-card')
        ], width=6)
    ], className="mb-4"),
    
    # KPI Cards
    dbc.Row(id='kpi-cards', className="mb-4"),
    
    # Main Charts Row 1
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='priority-pie-chart')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='volume-distribution')
        ], width=6)
    ], className="mb-4"),
    
    # Main Charts Row 2  
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='order-frequency-analysis')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='customer-segmentation')
        ], width=6)
    ], className="mb-4"),
    
    # Business Intelligence Section
    dbc.Row([
        dbc.Col([
            html.Div(id='business-insights')
        ])
    ], className="mb-4"),
    
    # Detailed Data Table
    dbc.Row([
        dbc.Col([
            html.H4("📊 Customer Details", className="mb-3"),
            html.Div(id='customer-table')
        ])
    ])
    
], fluid=True)

# Callbacks
@app.callback(
    [Output('state-overview-card', 'children'),
     Output('kpi-cards', 'children'),
     Output('priority-pie-chart', 'figure'),
     Output('volume-distribution', 'figure'),
     Output('order-frequency-analysis', 'figure'),
     Output('customer-segmentation', 'figure'),
     Output('business-insights', 'children'),
     Output('customer-table', 'children')],
    [Input('state-selector', 'value')]
)
def update_dashboard(selected_state):
    # Filter data for selected state
    state_data = df[df['State'] == selected_state].copy()
    
    if state_data.empty:
        # Return empty components if no data
        return [html.P("No data available") for _ in range(8)]
    
    # State Overview Card
    state_info = state_insights.get(selected_state, {})
    overview_card = dbc.Card([
        dbc.CardBody([
            html.H5(f"{state_info.get('full_name', selected_state)}", className="card-title"),
            html.P(f"Key Cities: {state_info.get('key_cities', 'N/A')}", className="small text-muted")
        ])
    ], color="primary", outline=True)
    
    # KPI Cards
    total_customers = len(state_data)
    avg_volume = state_data['Order vol / month'].mean()
    p1_customers = len(state_data[state_data['Priority'] == 'P1'])
    total_volume = state_data['Order vol / month'].sum()
    
    kpi_cards = [
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{total_customers:,}", className="card-title text-center text-primary"),
                    html.P("Total Customers", className="card-text text-center")
                ])
            ], className="h-100")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{p1_customers:,}", className="card-title text-center text-success"),
                    html.P("P1 Customers", className="card-text text-center")
                ])
            ], className="h-100")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{avg_volume:.1f}", className="card-title text-center text-info"),
                    html.P("Avg Volume/Month", className="card-text text-center")
                ])
            ], className="h-100")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{total_volume:.0f}", className="card-title text-center text-warning"),
                    html.P("Total Volume", className="card-text text-center")
                ])
            ], className="h-100")
        ], width=3)
    ]
    
    # 1. Priority Distribution Pie Chart
    priority_counts = state_data['Priority'].value_counts()
    fig1 = px.pie(
        values=priority_counts.values,
        names=priority_counts.index,
        title=f"Priority Distribution - {selected_state}",
        color=priority_counts.index,
        color_discrete_map=priority_colors
    )
    fig1.update_traces(textinfo='percent+label+value')
    fig1.update_layout(height=400, showlegend=True)
    
    # 2. Volume Distribution by Priority
    fig2 = px.box(
        state_data,
        x='Priority',
        y='Order vol / month',
        color='Priority',
        title=f"Order Volume Distribution by Priority - {selected_state}",
        color_discrete_map=priority_colors
    )
    fig2.update_layout(height=400)
    
    # 3. Order Frequency Analysis
    fig3 = px.scatter(
        state_data,
        x='Order # / month',
        y='Order vol / month',
        color='Priority',
        size='Order month #',
        title=f"Order Frequency vs Volume - {selected_state}",
        color_discrete_map=priority_colors,
        hover_data=['Company GSTIN']
    )
    fig3.update_layout(height=400)
    
    # 4. Customer Segmentation Heatmap
    # Create a crosstab for heatmap
    volume_bins = pd.cut(state_data['Order vol / month'], 
                        bins=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    freq_bins = pd.cut(state_data['Order # / month'], 
                      bins=3, labels=['Low Freq', 'Medium Freq', 'High Freq'])
    
    heatmap_data = pd.crosstab(volume_bins, freq_bins, normalize='all') * 100
    
    fig4 = px.imshow(
        heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        title=f"Customer Segmentation Matrix - {selected_state}",
        color_continuous_scale='Blues',
        text_auto='.1f'
    )
    fig4.update_layout(height=400)
    
    # Business Insights
    insights = dbc.Card([
        dbc.CardHeader([
            html.H4(f"🎯 Business Intelligence: {state_info.get('full_name', selected_state)}")
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H6("Market Focus", className="text-primary"),
                    html.P(state_info.get('market_focus', 'General market')),
                    
                    html.H6("Key Challenges", className="text-danger"),
                    html.P(state_info.get('challenges', 'Standard market challenges')),
                ], width=6),
                dbc.Col([
                    html.H6("Growth Opportunities", className="text-success"),
                    html.P(state_info.get('opportunities', 'Market expansion opportunities')),
                    
                    html.H6("Customer Insights", className="text-info"),
                    html.P(f"• P1 customers represent {(p1_customers/total_customers)*100:.1f}% of base"),
                    html.P(f"• Average order volume: {avg_volume:.1f} MT/month"),
                    html.P(f"• Priority distribution varies significantly across volume segments")
                ], width=6)
            ])
        ])
    ])
    
    # Customer Table
    table_data = state_data[['Company GSTIN', 'Priority', 'Order vol / month', 
                            'Order # / month', 'Order month #']].head(10)
    
    customer_table = dbc.Table.from_dataframe(
        table_data, 
        striped=True, 
        bordered=True, 
        hover=True,
        size='sm',
        className="mt-3"
    )
    
    return (overview_card, kpi_cards, fig1, fig2, fig3, fig4, insights, customer_table)


server = app.server

if __name__ == '__main__':
    app.run(debug=True)
