# -*- coding: utf-8 -*-


__author__ = 'aeiwz'

import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly.express as px
import dash

class plot_spectra:


    def __init__(self, data, x, y, title, xlabel, ylabel, color, width, height):
        
        import plotly.graph_objects as go
        import numpy as np
        import pandas as pd
        import plotly.express as px
        import dash


        self.data = data
        self.x = x
        self.y = y
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.color = color
        self.width = width
        self.height = height


        #plot spectra
        fig = go.Figure()
        for i in df3.index:
            fig.add_trace(go.Scatter(x=ppm, y=df3.loc[i,:], mode='lines', name=i, line=dict(color=line_color[i], width=1.5)))

        fig.update_layout(
            autosize=False,
            width=3000,
            height=1000,
            margin=dict(
                l=50,
                r=50,
                b=100,
                t=100,
                pad=4
            )
        )

        #add line tick of Y and X axis

        fig.update_xaxes(showline=True, showgrid=False, linewidth=1, linecolor='rgb(82, 82, 82)', mirror=True)
        fig.update_yaxes(showline=True, showgrid=False, linewidth=1, linecolor='rgb(82, 82, 82)', mirror=True)

        #Set font size of label
        fig.update_layout(font=go.layout.Font(size=20))
        #Add title
        fig.update_layout(title={'text': 'Medien Spectra'}, 
                        title_x=0.5, 
                        xaxis_title="δ <sup>1</sup>H", yaxis_title="Intensity",
                        title_font_size=28,
                        title_yanchor="top",
                        title_xanchor="center")


                        

        #Invert x-axis
        fig.update_xaxes(autorange="reversed")
        #Alpha background
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
        #fig.update_layout(title='Medien Spectra', xaxis_title='δ <sup>1</sup>H', yaxis_title='Intensity')
        #Y axis scale unite as scientific style decimal 4 digit

        fig.update_yaxes(tickformat='e')

        fig.show()
        fig.write_html(f'{project}.html')
