

Highcharts.chart('container-a', {


    title: {
        text: 'Pixel Intensity Graph of RGB channels'
    },

    subtitle: {
        text: 'Source: March-30 Dataset/50Hz-100FPS'
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
        data: MEAN_BLUE_LEVELS,
        color: '#0000FF'
    }, 
    {
        name: 'Red Pixel Intensity',
        data: MEAN_RED_LEVELS,
        color: '#FF0000'
    }, {
        name: 'Green Pixel Intensity',
        data: MEAN_GREEN_LEVELS,
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
        data: MEAN_BLUE_LEVELS,
        color: '#0000FF'
    }, {
        name: 'Threshold',
        data: THRESHOLD,
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
        name: 'Transmitted Bits',
        data: TRANSMITTED_BITS,
        color: '#FF0000'
    }, {
        name: 'Received Bits',
        data: RECEIVED_BITS,
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
