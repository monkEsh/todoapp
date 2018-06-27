function get_tasks() {
    $.ajax({
    url: "/portal/todo/",
    type: 'GET',
    dataType: 'json',
    success: function(res) {
            update_tasks(res);
        }
    });
}

function search_task() {
    // alert("Inside search");
    var q = $("#taskSearch").val();
    $.ajax({
    url: "/portal/todo/?q="+ q ,
    type: 'GET',
    dataType: 'json',
    success: function(res) {
            console.log(res);
            update_tasks(res);
        }
    });

}

function update_tasks(res) {
    var tasks = res.length;
    var id = $("#btasks");
    var divhtml = "";
    // console.log(res);
    for(x=0; x<tasks; x++){
        var title = res[x].title;
        var created = res[x].created;
        var creator = res[x].creator.username;
        var row = "<tr>\n" +
            "          <th scope=\"row\">"+ (x+1) +"</th>\n" +
            "          <td><a href='/portal/todo-tasks/"+ title +"'>"+ title +"</a></td>\n" +
            "          <td>"+ creator +"</td>\n" +
            "          <td>"+ created +"</td>\n" +
            "      </tr>";
        divhtml = divhtml + row;
    }
    id.html(divhtml);
}


function add_task(task) {
    var object = new Object();
    title = $("#id_title").val();
    status = $("#id_status").val();
    desc = $("#id_description").val();
    object.tasklist = task;

    if(title != "" && status != "" && desc != ""){
        object.title = title;
        object.status = status;
        object.desc = desc;
        $.ajax({
        url: "/portal/add-task/",
        type: 'POST',
        dataType: 'json',
            data: object,
        success: function(res) {
                if(res.success === true){
                    alert(res.message);
                    window.location.href = "/portal/todo-tasks/" + task;
                }
                else {
                    alert(res.message);
                }
            }
        });
    }
    else {
        alert("All Fields are required")
    }
}

function add_task_list() {
    var object = new Object();
    title = $("#id_title").val();

    if(title!=""){
        object.title = title;
        $.ajax({
        url: "/portal/add_task_list/",
        type: 'POST',
        dataType: 'json',
            data: object,
        success: function(res) {
                if(res.success === true){
                    alert(res.message);
                    window.location.href = "/portal/index/";
                }
                else {
                    alert(res.message);
                }
            }
        });
    }
    else{
        alert("Please provide title ")
    }
}

function get_task_updates(task) {
    $.ajax({
        url: "/portal/todo-list/?q=" + task,
        type: "GET",
        success: function (res) {
            console.log(res);
            update_task_table(res[0].task);
        }
    });
}

function update_task_table(res) {
    var task_table = $("#task_table");
    var len_task = res.length;
    var tbody = "";
    for(var x=0; x<len_task; x++){
        var action = res[x]["action_taken"];
        var user = res[x]["user"]["username"];
        var time = res[x]["time"];

        var row = "<tr>\n" +
            "<td>" + action + "</td>" +
            "<td>" + user + "</td>" +
            "<td>" + time + "</td>" +
            "</tr>";
        tbody = tbody + row;
    }
    task_table.html(tbody);
}


function update_task(col, title, tasklist) {
    var obj = new Object();
    obj.title = title;
    obj.col = col;

    if(col === 'title'){
        value = $("#id_title").val();
        title = value;
    }
    else if(col === 'description'){
        value = $("#id_description").val();
    }
    else if(col === 'status'){
        value =  $("#id_status").val();
        console.log(value);
    }
    obj.value = value;
    $.ajax({
        url: "/portal/edit-task-data/",
        type: "POST",
        data: obj,
        dataType: 'json',
        success: function (res) {
            if(res.success === true){
                alert(res.message);
                window.location.href = "/portal/edit-task/?tasklist=" + tasklist + "&task=" + title;
            }
            else {
                alert(res.message);
            }
        }
    });
}