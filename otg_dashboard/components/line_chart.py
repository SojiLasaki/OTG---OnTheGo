import pandas as pd
import plotly.express as px

def create_line_chart_from_csv(
    csv_path, 
    x_col, 
    y_col, 
    title="Line Chart", 
    color_col=None
):
    """
    Create a reusable Plotly line chart from a CSV file.

    Parameters:
        csv_path (str): Path to the CSV file
        x_col (str): Column name for the x-axis
        y_col (str): Column name for the y-axis
        title (str): Chart title
        color_col (str, optional): Column for grouping lines by color

    Returns:
        fig (plotly.graph_objs._figure.Figure): A Plotly Figure object
    """
    # Read CSV into DataFrame
    df = pd.read_csv(csv_path)
    
    # Create line chart
    fig = px.line(
        data_frame=df,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        markers=True
    )

    # Optional styling
    fig.update_layout(
        template="plotly_white",
        title_font=dict(size=20, color="black"),
        xaxis_title=x_col.capitalize(),
        yaxis_title=y_col.capitalize(),
        hovermode="x unified",
        legend_title_text=color_col.capitalize() if color_col else "",
    )

    return fig
