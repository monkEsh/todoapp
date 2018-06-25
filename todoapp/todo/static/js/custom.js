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
    object.title = $("#id_title").val();
    object.status = $("#id_status").val();
    object.desc = $("#id_description").val();
    object.tasklist = task;

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

function add_task_list() {
    var object = new Object();
    object.title = $("#id_title").val();
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