fetch('/static/forecast.json')
    .then(response => response.json())
    .then(forecastData => {
        // Prepare data for Plotly
        const trace = {
            x: forecastData.map(d => new Date(d.ds)),
            y: forecastData.map(d => d.yhat),
            mode: 'lines',
            name: 'Forecast',
            line: { color: 'rgba(0, 128, 255, 1)' },
        };

        const traceLower = {
            x: forecastData.map(d => new Date(d.ds)),
            y: forecastData.map(d => d.yhat_lower),
            mode: 'lines',
            name: 'Lower Bound',
            line: { width: 0 },
            fillcolor: 'rgba(0, 128, 255, 0.2)',
            fill: 'tonexty'
        };

        const traceUpper = {
            x: forecastData.map(d => new Date(d.ds)),
            y: forecastData.map(d => d.yhat_upper),
            mode: 'lines',
            name: 'Upper Bound',
            line: { width: 0 },
            fillcolor: 'rgba(0, 128, 255, 0.2)',
            fill: 'tonexty'
        };

        const layout = {
            title: '',
            xaxis: { 
                title: 'Time',
                titlefont: { size: 18, color: 'black', family: 'Arial, sans-serif', weight: 'bold' },
                tickfont: { size: 14, color: 'black', family: 'Arial, sans-serif' },
                showline: true,
                linecolor: 'black',
                linewidth: 2,
                side: 'under'
            },
            yaxis: { 
                title: 'Price',
                titlefont: { size: 18, color: 'black', family: 'Arial, sans-serif', weight: 'bold' },
                tickfont: { size: 14, color: 'black', family: 'Arial, sans-serif' },
                titlestandoff: 40,
                showline: true,
                linecolor: 'black',
                linewidth: 2,
            },
            showlegend: false,
            autosize: true,
            width: window.innerWidth * 0.95,
            height: window.innerHeight * 0.8,
            margin: { l: 50, r: 50, b: 100, t: 100, pad: 4 },
            plot_bgcolor: 'white',
            paper_bgcolor: 'white'
        };

        // Create the plot
        Plotly.newPlot('forecast', [traceLower, trace, traceUpper], layout);
    });
