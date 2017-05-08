var key_map = {
    100 : 'dirRight',
    115 : 'dirDown',
    97 : 'dirLeft',
    119 : 'dirUp',
    49 : 'infoStartPoint',
    50 : 'infoTelPoint',
    51 : 'infoWall',
    52 : 'infoDonGo',
    53 : 'infoBoss'
};
var dir_map = {
    1 : 'dirUp',
    2 : 'dirRight',
    3 : 'dirDown',
    4 : 'dirLeft'
};
var dicer_type_map = {
    W : "휠윈드",
    K : "관통",
    G : "근접",
    J : "저격",
    M : "마법",
    P : "폭격"
};
function make_svg_element(element){
    return document.createElementNS("http://www.w3.org/2000/svg", element);
}
function move_point(pos, move, ret){
    pos[0] = pos[0] + move[0];
    pos[1] = pos[1] + move[1];
    ret = ret + pos[0] + "," + pos[1] + " ";
    return ret;
}
function make_arrow_element(x, y, dir, size){
    var s_x = 20;
    var s_y = 20;
    var w = 40;
    var h = 40;
    var pos = [s_x+x*(w+10)+w/2, s_y+y*(h+10)+h/2];
    var points = "";
    points = move_point(pos, [-size/2, +size/2], points);
    points = move_point(pos, [size, 0], points);
    points = move_point(pos, [-size/2, -size*0.7], points);
    var new_poly = make_svg_element('polyline');
    $(new_poly).attr('points', points);
    var dir_class = dir_map[dir];
    $(new_poly).addClass(dir_class);
    $(new_poly).addClass("mapArrow");
    $(new_poly).attr("id", "mapArrow"+x+"x"+y);
    $('#mapInfo').append(new_poly);
}
function make_square_element(x, y) {
    var s_x = 20;
    var s_y = 20;
    var w = 40;
    var h = 40;
    var newElement = make_svg_element('rect');
    $(newElement).attr('x', s_x + x * (w + 10)).attr('y', s_y + y * (h + 10));
    $(newElement).attr('width', w).attr('height', h);
    $(newElement).addClass("mapRect");
    $(newElement).attr("id", "mapBase" + x + "x" + y);
    newElement.addEventListener('focus', function () {
        this.addEventListener('keypress', function (e) {
            var key = e.keyCode;
            var position = $(this).attr("id").replace("mapBase", "").split('x');
            var x = parseInt(position[0]);
            var y = parseInt(position[1]);
            if (is_dir(key)) {
                for(var dir_key in dir_map)
                    $(this).removeClass(dir_map[dir_key]);
                $('#mapArrow' + x + 'x' + y).remove();
            }
            var adding_class = "";
            if(key in key_map){
                adding_class = key_map[key];
                $(this).addClass(adding_class);
            }
            else
                console.log("Undefined Key : "+key);
            for(var dir_key in dir_map){
                if(adding_class == dir_map[dir_key]){
                    make_arrow_element(x, y, dir_key, 10);
                }
            }
        });
    }, newElement);

    return newElement;
}
function draw_base_map(){
    var x_max = parseInt($("#inputMapWidth").val());
    var y_max = parseInt($("#inputMapHeight").val());
    $('#Main_Control').attr('width', 20*2+40*x_max+10*(x_max-1));
    $('#Main_Control').attr('height', 20*2+40*y_max+10*(y_max-1));
    $('.mapRect').remove();
    for(var y=0;y<y_max;y++){
        for(var x=0;x<x_max;x++){
            $('#mapBase').append(make_square_element(x, y));
        }
    }
}
function save_map(){
    var x_max = parseInt($("#inputMapWidth").val());
    var y_max = parseInt($("#inputMapHeight").val());
    var data = [];
    var data_info = {
        "infoStartPoint" : [],
        "infoTelPoint" : [],
        "infoWall" : [],
        "infoDonGo" : [],
        "infoBoss" : []
    };
    var data_dicer = [];
    for(var y=0;y<y_max;y++){
        var row = [];
        for(var x=0;x<x_max;x++){
            var dir = 0;
            var classes = $('#mapBase'+x+"x"+y).attr("class");
            classes = classes.split(" ");
            var cl;
            var regex_dir = /dir*/;
            var regex_info = /info*/;
            for(var i=0;i<classes.length;i++){
                cl = classes[i];
                if(regex_dir.test(cl)){
                    for(var dir_key in dir_map){
                        if(cl == dir_map[dir_key]){
                            dir = dir_key;
                        }
                    }
                }
                if(regex_info.test(cl)){
                    data_info[cl].push([x, y]);
                }
            }
            row.push(dir);
        }
        data.push(row);
    }
    $(".dicerInfo").each(function(){
        var row = [];
        for(var i=0;i<3;i++){
            row.push($(this).find('td').eq(i).text());
        }
        data_dicer.push(row);
    });
    var map_size = [x_max, y_max];
    var send_data = {"mapSize" : map_size, "mapData" : data, "mapInfo" : data_info, "dicer" : data_dicer};
    $.ajax({
        url:"/_saveData",
        type:"POST",
        contentType:"application/json",
        dataType:"json",
        data: JSON.stringify(send_data),
        success:function(result){
            console.log(result);
        }
    });
}
function load_map(){
    $.ajax({
        url:"/_loadData",
        type:"POST",
        contentType:"application/json",
        dataType:"json",
        success:function(result){
            var get_data = result["mapData"];
            var x_max = result["mapSize"][0];
            var y_max = result["mapSize"][1];
            $("#inputMapWidth").val(x_max);
            $("#inputMapHeight").val(y_max);
            draw_base_map();
            for(var y=0;y<y_max;y++) {
                for (var x = 0; x < x_max; x++) {
                    var cl;
                    var dir = get_data[y][x];
                    $('#mapBase' + x + "x" + y).addClass(dir_map[dir]);
                    if (dir != 0)
                        make_arrow_element(x, y, dir, 10);
                }
            }
            var mapInfo = result["mapInfo"];
            for(var key in mapInfo){
                var positions = mapInfo[key];
                for(var i=0;i<positions.length;i++){
                    var x = positions[i][0];
                    var y = positions[i][1];
                    $('#mapBase'+x+'x'+y).addClass(key);
                }
            }
            var dicer_info = result['dicer'];
            for(var i=0;i<dicer_info.length;i++)
            {
                add_dicer_info_sub(dicer_info[i]);
            }
        }
    });
}
function is_dir(key){
    if((key==100)|(key==115)|(key==97)|(key==119))
        return true;
    else
        return false;
}
function add_dicer_info_sub(data){
    var new_row = $('<tr class="dicerInfo"></tr>');
    for(var i=0;i<3;i++){
        $(new_row).append($('<td></td>').append(data[i]));
    }
    var new_delete_btn = $('<input type="button" class="btn btn-default btn-sm" value="Delete">');
    $(new_delete_btn).click(function(){
        $(this).parent().parent().remove();
    });
    $(new_row).append($('<td></td>').append(new_delete_btn));
    $('#dicerInfo').append(new_row);
}
function add_dicer_info(){
    var str = $('#inputDicer').val();
    str = str.split(' ');
    if(str.length != 3){
        alert("정확한 정보를 입력하세요");
        return;
    }
    if(str[1] in dicer_type_map){
        str[1] = dicer_type_map[str[1]];
    }
    else{
        alert("정확한 정보를 입력하세요(Dicer type)");
        return;
    }
    add_dicer_info_sub(str);
    $('#inputDicer').val("");
}
function start_lod(){
    console.log("start LOD");
    var send_data = {move : 0};
    $.ajax({
        url:"/_run",
        type:"POST",
        contentType:"application/json",
        dataType:"json",
        data: JSON.stringify(send_data),
        success:function(result){
            var s_x = 20;
            var s_y = 20;
            var w = 40;
            var h = 40;
            var x = result["move_data"][0];
            var y = result["move_data"][1];
            console.log(x, y);
            console.log(result);
            var newElement = make_svg_element('circle');
            $(newElement).attr('cx', s_x + x * (w + 10) + w/2).attr('cy', s_y + y * (h + 10) +h/2).attr('r', 10);
            $(newElement).attr("id", "master");
            $('#Main_Control').append(newElement);
        }
    });
}
function move_lod(){
    var send_data = {move : 1};
    $.ajax({
        url:"/_run",
        type:"POST",
        contentType:"application/json",
        dataType:"json",
        data: JSON.stringify(send_data),
        success:function(result){
            var s_x = 20;
            var s_y = 20;
            var w = 40;
            var h = 40;
            var x = result["move_data"][0];
            var y = result["move_data"][1];
            console.log(x, y);
            console.log(result);
            $('#master').attr('cx', s_x + x * (w + 10) + w/2).attr('cy', s_y + y * (h + 10) +h/2).attr('r', 10);
        }
    });
}


$(document).ready(function() {
    //draw_base_map();
    load_map();
    $('#inputMapWidth').change(draw_base_map);
    $('#inputMapHeight').change(draw_base_map);
    $('#inputSaveButton').click(save_map);
    $('#inputLoadButton').click(load_map);
    $('#inputDicerButton').click(add_dicer_info);
    $('#inputDicer').bind("enterKey",add_dicer_info);
    $('#inputDicer').keyup(function(e){
        if(e.keyCode == 13)
            $(this).trigger("enterKey");
    });
    $('#hideMapPicture').click(function(){$('#panelMapPicture').toggle('show');});
    $('#hideGuide').click(function(){$('#panelGuide').toggle('show');});
    $('#hideInfo').click(function(){$('#panelInfo').toggle('show');});
    $('#inputStartButton').click(start_lod);
    $('#inputMoveButton').click(move_lod);
});
