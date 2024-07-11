# -*- coding: utf-8 -*-

__auther__ = 'aeiwz'


#Peak picking all spectra and plot using scipy and pyplot

from scipy.signal import find_peaks
import matplotlib.pyplot as plt


def peak_picking(spectra, ppm, threshold=0.05, min_dist=100):
    
        peaks = []
        for i in range(spectra.shape[0]):
            y = spectra.iloc[i,:]
            peaks_, _ = find_peaks(y, height=threshold, distance=min_dist)
            peaks.append(peaks_)
    
        return peaks

peaks = peak_picking(spectra, ppm, threshold=0.05, min_dist=1000)


def plot_peaks(spectra, ppm, peaks, color_map=None, title='Peak picking', title_font_size=28, legend_name='<b>Group</b>', legend_font_size=20, axis_font_size=20, fig_height = 800, fig_width = 2000, line_width = 1.5, legend_order=None):
    
        from plotly import graph_objs as go
        from plotly import express as px
    

    
        #plot spectra
        fig = go.Figure()
        for i in range(spectra.shape[0]):
            fig.add_trace(go.Scatter(x=ppm, y=spectra.iloc[i,:], mode='lines', name=spectra.index[i], line=dict(width=line_width)))
            fig.add_trace(go.Scatter(x=ppm[peaks[i]], y=spectra.iloc[i,peaks[i]], mode='markers', marker=dict(size=5), showlegend=False))

        fig.update_layout(
            autosize=False,
            width=fig_width,
            height=fig_height,
            margin=dict(
                l=50,
                r=50,
                b=100,
                t=100,
                pad=4
            )
        )

        fig.update_xaxes(showline=True, showgrid=False, linewidth=1, linecolor='rgb(82, 82, 82)', mirror=True)
        fig.update_yaxes(showline=True, showgrid=False, linewidth=1, linecolor='rgb(82, 82, 82)', mirror=True)

        #Set font size of label
        fig.update_layout(font=go.layout.Font(size=axis_font_size))
        #Add title
        fig.update_layout(title={'text': title, 'xanchor': 'center', 'yanchor': 'top'}, 
                        title_x=0.5, 
                        xaxis_title="<b>δ<sup>1</sup>H</b>", yaxis_title="<b>Intensity</b>",
                        title_font_size=title_font_size,
                        title_yanchor="top",
                        title_xanchor="center")

        #Add legend

        fig.update_layout(legend=dict( title=legend_name, font=dict(size=legend_font_size)))
        #Invert x-axis
        fig.update_xaxes(autorange="reversed")

        #Alpha background
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
        fig.update_layout(title='Medien Spectra', xaxis_title='δ <sup>1</sup>H', yaxis_title='Intensity')

        #set y-axis tick format to scientific notation with 4 decimal places
        fig.update_layout(yaxis=dict(tickformat=".2e"))

        return fig

plot_peaks(spectra, ppm, peaks, color_map=color_dict_)



import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html

class pickie_peak:
    def __init__(self, spectra: pd.DataFrame, ppm: list):
        self.spectra = spectra
        self.ppm = ppm

    def run_ui(self):
        class plot_NMR_spec:
            def __init__(self, spectra, ppm):
                self.spectra = spectra
                self.ppm = ppm

            def single_spectra(self, color_map=None, 
                                title='<b>Spectra of <sup>1</sup>H NMR data</b>', title_font_size=28, 
                                legend_name='<b>Group</b>', legend_font_size=20, 
                                axis_font_size=20, 
                                line_width=1.5, legend_order=None):
                from plotly import express as px

                spectra = self.spectra
                ppm = self.ppm

                df_spectra = pd.DataFrame(spectra)
                df_spectra.columns = ppm

                if color_map is None:
                    color_map = dict(zip(df_spectra.index, px.colors.qualitative.Plotly))
                else:
                    if len(color_map) != len(df_spectra.index):
                        raise ValueError('Color map must have the same length as group labels')

                fig = go.Figure()
                for i in df_spectra.index:
                    fig.add_trace(go.Scatter(x=ppm, y=df_spectra.loc[i, :], mode='lines', name=i, line=dict(width=line_width)))

                fig.update_layout(
                    autosize=True,
                    margin=dict(l=50, r=50, b=100, t=100, pad=4)
                )

                fig.update_xaxes(showline=True, showgrid=False, linewidth=1, linecolor='rgb(82, 82, 82)', mirror=True)
                fig.update_yaxes(showline=True, showgrid=False, linewidth=1, linecolor='rgb(82, 82, 82)', mirror=True)

                fig.update_layout(
                    font=go.layout.Font(size=axis_font_size),
                    title={'text': title, 'xanchor': 'center', 'yanchor': 'top'},
                    title_x=0.5,
                    xaxis_title="<b>δ<sup>1</sup>H</b>", yaxis_title="<b>Intensity</b>",
                    title_font_size=title_font_size,
                    title_yanchor="top",
                    title_xanchor="center",
                    legend=dict(title=legend_name, font=dict(size=legend_font_size)),
                    xaxis_autorange="reversed",
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    yaxis=dict(tickformat=".2e")
                )

                return fig

        # Instantiate the class
        plotter = plot_NMR_spec(self.spectra, self.ppm)

        # Create the Dash app with Bootstrap stylesheet
        app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

        # Layout for the app
        app.layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='nmr-plot',
                        figure=plotter.single_spectra()
                    ),
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div(id='peak-data', children='Click on the plot to select peaks.'),
                    dcc.Store(id='stored-peaks', data=[]),
                    dbc.Button("Export X Positions", id="export-button", color="primary", className="mt-2"),
                    dbc.Button("Clear Data", id="clear-button", color="danger", className="mt-2 ml-2"),
                    dcc.Download(id="download-dataframe-csv")
                ], width=12)
            ])
        ], fluid=True)

        @app.callback(
            [Output('stored-peaks', 'data'), Output('peak-data', 'children')],
            [Input('nmr-plot', 'clickData'), Input('clear-button', 'n_clicks')],
            [State('stored-peaks', 'data')]
        )
        def update_peaks(clickData, clear_clicks, stored_peaks):
            ctx = dash.callback_context

            if not ctx.triggered:
                return stored_peaks, 'Click on the plot to select peaks.'
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            if button_id == 'clear-button':
                return [], 'Click on the plot to select peaks.'

            if clickData:
                click_point = clickData['points'][0]
                x_peak = click_point['x']
                y_peak = click_point['y']
                stored_peaks.append({'x': x_peak, 'y': y_peak})
                peak_text = f'Picked peaks (X): {[p["x"] for p in stored_peaks]}'
                return stored_peaks, peak_text

            return stored_peaks, 'Click on the plot to select peaks.'

        @app.callback(
            Output("download-dataframe-csv", "data"),
            [Input("export-button", "n_clicks")],
            [State("stored-peaks", "data")],
            prevent_initial_call=True
        )
        def export_x_positions(n_clicks, stored_peaks):
            if not stored_peaks:
                return dash.no_update

            x_positions = [p['x'] for p in stored_peaks]
            df = pd.DataFrame(x_positions, columns=["X Positions"])
            csv_string = df.to_csv(index=False)

            return dict(content=csv_string, filename="x_positions.csv")

        if __name__ == '__main__':
            app.run_server(debug=True)

