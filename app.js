var app = (function(){
    // 设置常量配置信息
    const FILE_PATH = 'total_data.json' // 主要数据的存储文件
    // 大标题的关键字
    const SECTION_LIST = [
        'human_resource','finance','material','agriculture','industry',
        'commerce', 'big_data','internet','ai','legal'
    ]
    const TITLE_LINE_CHART = {
        'china': {
            'title':'100指数折线图',
            'xAxis': ['第一周\n(06.29-07.05)','第二周\n(07.06-07.12)','第三周\n(07.13-07.19)']
            },
        'indonesia': {
            'title': '100 Grafik Garis Indeks',
            'xAxis': ['week1\n(06.29-07.05)','week2\n(07.06-07.12)','week3\n(07.13-07.19)']
        },
        'double': {
            'title': '100 Grafik Garis Indeks\n100指数折线图',
            'xAxis': ['week1\n(06.29-07.05)','week2\n(07.06-07.12)','week3\n(07.13-07.19)']
        },
    }
    const TEXT_BUTTON_LINE_CHART = {
        'china': '历史总分数',
        'indonesia': 'skor total sejarah',
        'double': 'skor total sejarah\n历史总分数'
    }
    // 每个时间段对应的日期
    const TANGGAL = {
        "week1" : "2024.06.29 - 2024.07.05",
        "week2" : "2024.07.06 - 2024.07.12",
        "week3" : "2024.07.13 - 2024.07.19",
        "week4" : "2024.07.20 - 2024.07.26",
        "month" : "2024.07.01 - 2024.07.30"
    }

    // 设置变量
    // 时间段
    let period = {
        'year': '2024',
        'month': '7',
        'period': 'week3'
    } 
    // 语言
    let language = 'china' 
    // 计算得分的数据结构
    let section_score= {
        'human_resource':0,
        'finance':0,
        'material':0,
        'agriculture':0,
        'industry':0,
        'commerce':0, 
        'big_data':0,
        'internet':0,
        'ai':0,
        'legal':0
    }

    // 函数：大标题缩放功能
    cs = function(section){
        $('thead#'+section).click(function(){
            var tbody = $('tbody#'+section)
            var singal = tbody.attr('class')
            if(singal == 'active'){
            tbody.attr('style','display:none')
            tbody.attr('class','inactive')
            }else{
            tbody.attr('style','')
            tbody.attr('class','active')
            tbody_list = $('tbody')
            // 展开一项大标题时，收缩其他大标题的二级标题
            for(var i = 0; i < tbody_list.length; i++){
                if(tbody_list[i].id != section){
                tbody_list[i].style.display = 'none'
                tbody_list[i].classList.remove('active')
                tbody_list[i].classList.add('inactive')
                }
            }
            // console.log(tbody_list)
            }
        })
        // 注释缩放功能
        $('tbody#'+section).on('click', '[id^="data_"]', function(){
            var index = this.id.split('_')[1];
            tr_commen = $(`tr#commen_${index}_${section}`)
            var singal = tr_commen.attr('class')
            if(singal == 'active'){
            tr_commen.attr('style','display:none;')
            tr_commen.attr('class','inactive')
            }else{
            tr_commen.attr('style','')
            tr_commen.attr('class','active')
            for (var i = 0; i < 10; i++){
                if( i != index){
                dom_other = $(`tr#commen_${i}_${section}`)
                dom_other.attr('style','display:none;')
                dom_other.attr('class','inactive')
                }
            }
            }
        })
    }

    // 函数：具体指标数据的填写
    function input_data(section, data_list){
        var section_score = 0
        var tbody = $('tbody#'+section)
        for(var index in data_list){
            var data = data_list[index]

            var add_tr  
            if(data[8] != 0){
            add_tr = 
            `<tr id="data_${index}_${section}">
            <td class="center" data-label="序号" colspan="1">${data[0]}</td>
            <td data-label="分项" colspan="2">${data[1]}</td>
            <td class="center" data-label="负责人" colspan="1">${data[2]}</td>
            <td class="center" data-label="单位" colspan="1">${data[3]}</td>
            <td class="center" data-label="前值" colspan="1">${data[4]}</td>
            <td class="center" data-label="预测值" colspan="1">${data[5]}</td>
            <td class="center" data-label="实际值" colspan="1">${data[6]}</td>
            <td class="center" data-label="分数" colspan="1">${data[8]}</td>
            </tr>
            <tr id="commen_${index}_${section}" class="inactive" style="display: none;">
            <td colspan="10">分析:\n ${data[9]}</td>
            </tr>
            `
            }else if(data[8] == 0){
            add_tr = 
            `<tr id="data_${index}_${section}" class='unhealthy_data'>
                <td class="center" data-label="序号" colspan="1">${data[0]}</td>
                <td data-label="分项" colspan="2">${data[1]}</td>
                <td class="center" data-label="负责人" colspan="1">${data[2]}</td>
                <td class="center" data-label="单位" colspan="1">${data[3]}</td>
                <td class="center" data-label="前值" colspan="1">${data[4]}</td>
                <td class="center" data-label="预测值" colspan="1">${data[5]}</td>
                <td class="center" data-label="实际值" colspan="1">${data[6]}</td>
                <td class="center" data-label="分数" colspan="1">${data[8]}</td>
            </tr>
            <tr id="commen_${index}_${section}" class="inactive" style="display: none;">
                <td colspan="10">分析:\n ${data[9]}</td>
            </tr>
            `
            }
            
            
            tbody.append(add_tr)
            section_score = section_score + data[8]
        }
        return section_score
        }

    function update_data(section, data_list, language){
        var section_score = 0
        for(var index in data_list){
        data = data_list[index]
        tr_data = $(`tr#data_${index}_${section}`)
        tr_commen = $(`tr#commen_${index}_${section}`)
        for(var i=1; i<9; i++){
            tr_child = tr_data.children(`td:nth-child(${i})`)
            if( i == 8){
            tr_child.text(data[i])
            if(data[i] == 0){
                tr_data.attr('style','color:red')
            }else if(data[i] != 0){
                tr_data.attr('style', 'color:black')
            }
            }else{
            tr_child.text(data[i-1])
            }
        }
        if(language == 'china'){
            tr_commen.children('td:nth-child(1)').text("分析:\n" + data[9])
        }else{
            tr_commen.children('td:nth-child(1)').text("Analisa:\n" + data[9])
        }
        
        section_score = section_score + data[8]
        }
        return section_score
    }

    // 将总得分写入指定位置
    function input_total_score(section_score,language){
        var total = 0
        for(var key in section_score){
            td_key = $('thead#'+key).find('tr:first').children('td:nth-child(4)')
            td_key.text(section_score[key])
            total = total + section_score[key]
        }
        if (language == 'china'){
            score_description = '总分数: '
        }else if (language == 'indonesia'){
            score_description = 'Total Score: '
        }else{
            score_description = 'Total Score: '
        }
        total_score = score_description + total
        $('h3#total_score').text(total_score)
    }

    // 渲染标题
    function get_title_data(language){
        // 获取数据
        var request = new XMLHttpRequest();
            request.open('get', FILE_PATH)
            request.send(null)
            request.onload = function(){
            var data = JSON.parse(request.responseText)
            data = data[period['year']][period['month']][period['period']][language]
            $('thead#total').children('tr:nth-child(1)').children('td:nth-child(1)').find('h3:first').text(data['title']['title'])

            section_title = data
            for(index in SECTION_LIST){
                section = SECTION_LIST[index]
                title = section_title[section]
                tr = $('thead#'+section).find("tr:first")
                tr.children("td:nth-child(1)").text(title["title"])
                tr.children("td:nth-child(2)").text(title["PIC"])
                tr.children("td:nth-child(3)").text(title["sekre"])
            }
            
            sub_title = data["title"]['subtitle']
            tbody_tr = $('tbody').find('tr:first')
            for(var i=1; i<=9; i++){
                if( i ==8 || i == 9){
                tbody_tr.children(`th:nth-child(${i})`).text(sub_title[i])
                }else{
                tbody_tr.children(`th:nth-child(${i})`).text(sub_title[i-1])
                }
                
            }
        }
    }

    // 函数：渲染数据
    input_period_data = function () {
        // 获取数据
        var score = 0
        var request = new XMLHttpRequest()
        request.open('get', FILE_PATH)
        request.send(null)
        request.onload = function(){
        var data = JSON.parse(request.responseText)
        data = data[period['year']][period['month']][period['period']][language]
        
        // 渲染数据
        for(index in SECTION_LIST){
            section = SECTION_LIST[index]
            section_score[section] = 0  //将分数置为零，防止累加之前计算的得分
            section_score[section] = input_data(section,data[section]['sub'])
        }
        // 渲染总分数
        input_total_score(section_score,language)
        }
    }

    // 只更新数据部分的数据
    function update_period_data(language) {
        // 获取数据
        var request = new XMLHttpRequest();
        request.open('get', FILE_PATH)
        request.send(null)
        request.onload = function(){
        var data = JSON.parse(request.responseText)
        data = data[period['year']][period['month']][period['period']][language]
        // 渲染数据
        for(index in SECTION_LIST){
            section = SECTION_LIST[index]
            section_score[section] = 0  //将分数置为零，防止累加之前计算的得分
            section_score[section] = update_data(section,data[section]['sub'],language)
        }
        // 渲染总分数
        input_total_score(section_score,language)
        }
    }

    // 更新Tema部分标题的语言
    function update_tema(language){
        tema_language = {
            'china': ['主题', '负责人', '追踪秘书', '分数'],
            'indonesia': ['Tema', 'PIC', 'PIC Follow-Up', 'Nilai'],
            'double': ['Tema\n主题', 'PIC\n负责人', 'PIC Follow-Up\n追踪秘书', 'Nilai\n分数']
        }

        tr_tema = $('tr#tema')
        for(var i=1; i<=4; i++){
            tr_tema.children(`td:nth-child(${i})`).text(tema_language[language][i-1])
        }
    }

    // 设置图表
    function setLineChart(){
        $.get('echart_data.js').done(function(data){
            lineChart.setOption({
                title: {
                text: TITLE_LINE_CHART[language]['title'],
                x:'center',
                y: 'top'
                },
                xAxis: {
                    type: 'category',
                    data: TITLE_LINE_CHART[language]['xAxis']
                },
                yAxis: {
                    type: 'value'
                },
                series: [{
                    data: [55, 65, 62],
                    type: 'line',
                    label:{
                        show: true,
                        position: 'bottom',
                        fontSize: 15
                    }
                }]
            })
        })
    }
})

export {app}