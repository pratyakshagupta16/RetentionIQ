import plotly.graph_objects as go
import plotly.express as px


BG_COLOR = "#0B1220"
CARD_COLOR = "#111827"
CYAN = "#93C5FD"
PURPLE = "#DDD6FE"
MAGENTA = "#FECDD3"
GRAY_TEXT = "#94A3B8"
WHITE_TEXT = "#E2E8F0"
GRID_COLOR = "#1E293B"

COLOR_PALETTE = ["#A7F3D0", "#93C5FD", "#DDD6FE", "#FED7AA", "#FECDD3"]

SEGMENT_COLORS = {
    "Champions": "#A7F3D0",
    "Loyal Customers": "#93C5FD",
    "Potential Loyalists": "#DDD6FE",
    "At Risk": "#FED7AA",
    "Lost Customers": "#FECDD3"
}

def apply_dark_theme(fig):



    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Roboto, sans-serif", color=WHITE_TEXT),
        title_font=dict(size=15, family="Inter, Roboto, sans-serif", color=WHITE_TEXT),
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(
            bgcolor="rgba(17, 24, 39, 0.7)",
            bordercolor=GRID_COLOR,
            borderwidth=1,
            font=dict(color=GRAY_TEXT)
        ),
        xaxis=dict(
            gridcolor=GRID_COLOR,
            linecolor=GRID_COLOR,
            zerolinecolor=GRID_COLOR,
            tickfont=dict(color=GRAY_TEXT)
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR,
            linecolor=GRID_COLOR,
            zerolinecolor=GRID_COLOR,
            tickfont=dict(color=GRAY_TEXT)
        ),
        hoverlabel=dict(
            bgcolor=CARD_COLOR,
            bordercolor=GRID_COLOR,
            font=dict(family="Inter, Roboto, sans-serif", color=WHITE_TEXT, size=12)
        )
    )
    return fig

def create_line_chart(df, x, y, title, x_label="", y_label="", color_hex=CYAN):



    fig = go.Figure()


    fig.add_trace(go.Scatter(
        x=df[x],
        y=df[y],
        mode="lines+markers",
        line=dict(color=color_hex, width=3),
        marker=dict(size=6, color=color_hex),
        name=y_label or y,
        fill="tozeroy",
        fillcolor=f"rgba({','.join([str(int(color_hex[i:i+2], 16)) for i in (1, 3, 5)])}, 0.08)"
    ))

    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label
    )

    return apply_dark_theme(fig)

def create_bar_chart(df, x, y, title, x_label="", y_label="", color_hex=PURPLE, horizontal=False, color_map=None):



    if horizontal:
        if color_map:
            fig = px.bar(df, x=x, y=y, orientation="h", title=title, color=y, color_discrete_map=color_map)
        else:
            fig = px.bar(df, x=x, y=y, orientation="h", title=title)
            fig.update_traces(marker_color=color_hex)
    else:
        if color_map:
            fig = px.bar(df, x=x, y=y, title=title, color=x, color_discrete_map=color_map)
        else:
            fig = px.bar(df, x=x, y=y, title=title)
            fig.update_traces(marker_color=color_hex)

    fig.update_traces(marker_line_color=CARD_COLOR, marker_line_width=1, opacity=0.85)
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label
    )
    return apply_dark_theme(fig)

def create_donut_chart(df, names, values, title, color_map=None):



    if color_map:
        fig = px.pie(
            df,
            names=names,
            values=values,
            title=title,
            hole=0.4,
            color=names,
            color_discrete_map=color_map
        )
    else:
        fig = px.pie(
            df,
            names=names,
            values=values,
            title=title,
            hole=0.4,
            color_discrete_sequence=COLOR_PALETTE
        )
    fig.update_traces(textposition="inside", textinfo="percent+label", marker=dict(line=dict(color=BG_COLOR, width=2)))
    return apply_dark_theme(fig)

def create_scatter_3d(df, x, y, z, color_col, title, hover_cols=None):



    hover_data = hover_cols if hover_cols else [x, y, z]
    fig = px.scatter_3d(
        df,
        x=x,
        y=y,
        z=z,
        color=color_col,
        color_discrete_sequence=COLOR_PALETTE,
        title=title,
        hover_data=hover_data
    )

    fig.update_layout(
        scene=dict(
            xaxis=dict(gridcolor=GRID_COLOR, backgroundcolor=BG_COLOR, color=WHITE_TEXT),
            yaxis=dict(gridcolor=GRID_COLOR, backgroundcolor=BG_COLOR, color=WHITE_TEXT),
            zaxis=dict(gridcolor=GRID_COLOR, backgroundcolor=BG_COLOR, color=WHITE_TEXT),
        )
    )
    return apply_dark_theme(fig)

def create_scatter_2d(df, x, y, color_col, title, hover_cols=None):



    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color_col,
        color_discrete_sequence=COLOR_PALETTE,
        title=title,
        hover_data=hover_cols
    )
    fig.update_traces(marker=dict(size=8, opacity=0.8, line=dict(width=1, color=BG_COLOR)))
    return apply_dark_theme(fig)

def create_box_plot(df, x, y, title, color_col=None):



    fig = px.box(
        df,
        x=x,
        y=y,
        color=color_col,
        color_discrete_sequence=COLOR_PALETTE,
        title=title
    )
    return apply_dark_theme(fig)

def create_heatmap(df_corr, title):



    fig = px.imshow(
        df_corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale=[[0, CARD_COLOR], [0.5, PURPLE], [1, CYAN]],
        title=title
    )
    return apply_dark_theme(fig)
