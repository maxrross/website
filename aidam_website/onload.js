async function fetchAndPlot() {
    // get data for figure 1
    const response1 = await fetch('http://localhost:3000/figure1');
    const data = await response1.json();
    const names = data.map(x => x.name);
    const counts = data.map(x => x.count);
    const trace = {values: counts, labels: names, marker: {colors: 'Electric'}, type: 'pie'};
    const layout = {title: 'Number of Data in Each Collection'};
    // plot figure 1
    Plotly.newPlot('plot1', [trace], layout);

    // get data for figure 2 and 3
    let response2 = await fetch('http://localhost:3000/figure2and3');
    const data2 = await response2.json();
    // process the data
    let data_uploaders={};
    let data_dates={};
    for (const d of data2){
        for (const _d of d['response']){
            data_uploaders[_d['_id']['uploader']] = (data_uploaders[_d['_id']['uploader']] ?? 0) + _d['count'];
            data_dates[_d['_id']['date']] = (data_dates[_d['_id']['date']] ?? 0) + _d['count'];
        }
    }
    const sorted_data_uploaders = Object.entries(data_uploaders)
    .sort((b, a) => b[1] - a[1])
    .reduce((obj, [key, value]) => {
      obj[key] = value;
      return obj;
    }, {});

    const layout2 = {title: 'All Time Data Record'};
    const trace2 = {y: Object.keys(sorted_data_uploaders), 
                    x: Object.values(sorted_data_uploaders), 
                    type: 'bar', orientation: 'h',
                    marker: {
                        color: 'rgba(50, 171, 96, 0.6)',
                        line: {
                          color: 'rgba(50, 171, 96, 1.0)',
                          width: 1
                        }
                      }};
    Plotly.newPlot('plot2', [trace2], layout2);

    const layout3 = {title: 'Trend of Data Generation'};
    const trace3 = {x: Object.keys(data_dates), 
                    y: Object.values(data_dates), 
                    type: 'scatter',
                    marker: {
                        color: 'rgb(17, 157, 255)',
                        size: 20,
                        line: {
                            color: 'rgb(231, 99, 250)',
                            width: 2
                          }
                        }};
    Plotly.newPlot('plot3', [trace3], layout3);
  }

window.onload = fetchAndPlot;
