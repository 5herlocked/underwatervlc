function loadData(){
    
    var option = document.getElementById("formaction");
    var val =  String(option.value);
    

   

Highcharts.chart('container-a', {


    title: {
        text: 'Pixel Intensity Graph of RGB channels'
    },

    subtitle: {
        text: 'Source' + String(val)
    },

    yAxis: {
        title: {
            text: 'Pixel Intensity'
        },
 
    },
  

    xAxis: {
        title: {
            text: 'Frame Number'
        },

    },
    tooltip: {
        style: {
            display: "none",
        },
        enabled: false
    },

    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    chart: {
        zoomType: 'x',

    },

    plotOptions: {
        series: {


            label: {
                connectorAllowed: false
            },
            pointStart: 1
        }
    },


    exporting: {
        showTable: false,
        csv: {
            columnHeaderFormatter: function (item, key) {
                if (!item || item instanceof Highcharts.Axis) {
                    return 'Frame'
                } else {
                    return item.name;
                }
            }
        }
    },

    series: [{
        name: 'Blue Pixel Intensitiy',
        data: window["meanBlueLevels_"  + val],
        color: '#0000FF'
    }, 
    {
        name: 'Red Pixel Intensity',
        data: window["meanRedLevels_"  + val],
        color: '#FF0000'
    }, {
        name: 'Green Pixel Intensity',
        data: window["meanGreenLevels_"  + val],
        color: '#00FF00'
    }],

    responsive: {
        rules: [{
            condition: {
                maxWidth: 500
            },
            chartOptions: {
                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'bottom'
                }
            }
        }]
    }

});


Highcharts.chart('container-b', {


    title: {
        text: 'Pixel Intensity Graph of Blue channel'
    },

    subtitle: {
        text: 'Source: March-30 Dataset/50Hz-100FPS'
    },

    yAxis: {
        title: {
            text: ' Blue Pixel Intensity'
        }
    },

    xAxis: {
        title: {
            text: 'Frame Number'
        },

    },
    tooltip: {
        style: {
            display: "none",
        },
        enabled: false
    },

    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    chart: {
        zoomType: 'x',

    },

    plotOptions: {
        series: {


            label: {
                connectorAllowed: false
            },
            pointStart: 1
        }
    },


    exporting: {
        showTable: false,
        csv: {
            columnHeaderFormatter: function (item, key) {
                if (!item || item instanceof Highcharts.Axis) {
                    return 'Frame'
                } else {
                    return item.name;
                }
            }
        }
    },

    series: [{
        name: 'Blue Pixel Intensitiy',
        data: window["meanBlueLevels_"  + val],
        color: '#0000FF'
    }, {
        name: 'Threshold',
        data: window["threshold_" + val],
        color: '#FF0000'
    }],

    responsive: {
        rules: [{
            condition: {
                maxWidth: 500
            },
            chartOptions: {
                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'bottom'
                }
            }
        }]
    }

});

Highcharts.chart('container-c', {


    title: {
        text: 'Transmitted Bits VS Received Bits'
    },

    subtitle: {
        text: 'Source:' + String(val)
    },

    yAxis: {
        title: {
            text: ' Blue Pixel Intensity'
        }
    },

    xAxis: {
        title: {
            text: 'Frame Number'
        },

    },
    tooltip: {
        style: {
            display: "none",
        },
        enabled: false
    },

    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    chart: {
        zoomType: 'x',

    },

    plotOptions: {
        series: {


            label: {
                connectorAllowed: false
            },
            pointStart: 1
        }
    },


    exporting: {
        showTable: false,
        csv: {
            columnHeaderFormatter: function (item, key) {
                if (!item || item instanceof Highcharts.Axis) {
                    return 'Frame'
                } else {
                    return item.name;
                }
            }
        }
    },

    series: [{
        name: 'Transmitted Bits',
        data: window["received_bits_" + val],
        color: '#FF0000'
    }, {
        name: 'Received Bits',
        data: window["threshold_" + val],
        color: '#0000FF'
    }],

    responsive: {
        rules: [{
            condition: {
                maxWidth: 500
            },
            chartOptions: {
                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'bottom'
                }
            }
        }]
    }

});

};