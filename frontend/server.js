// Some code taken from class lectures and homeworks.

// load the things we need
var express = require('express');
var app = express();
const bodyParser  = require('body-parser');

// required module to make calls to a REST API
const axios = require('axios');

app.use(bodyParser.urlencoded());

// set the view engine to ejs
app.set('view engine', 'ejs');

// index page 
app.get('/', function(req, res) {
    res.render("pages/index.ejs", {});
});

app.post('/process_login', function(req, res){
    var user = req.body.username;
    var password = req.body.password;
    // This sample is showing how to validate user input with static username and password
    // If you want to validate database user data then you need to call REST API for it to get user data
    // Then validate user input with user data retrived from database.
    if(user === 'admin' && password === 'password')
    { 
        res.render('pages/welcome.ejs', {
            user: user,
            auth: true
        });
        axios.post('http://127.0.0.1:5000/daycareauthentication', {
        auth: "true"
        });
    }
    else
    {
        res.render('pages/failed.ejs', {
            user: 'UNAUTHORIZED',
            auth: false
        });
    }
  });

app.get('/addfacility', function(req, res) {
    res.render("pages/addfacility.ejs", {});
  });

app.post('/formaddfacility', function(req, res) {
    res.render("pages/success.ejs", {});
    axios.post('http://127.0.0.1:5000/addfacility', {
        new_name: req.body.facname
    })
});

app.get('/viewfacility', function(req, res) {
    axios.get('http://127.0.0.1:5000/viewfacility')
    .then((response)=>{
        let facilities = response.data;

        res.render('pages/viewfacility.ejs', {
            facilities: facilities
        });
    });
});

app.get('/updatefacility', function(req, res) {
    axios.get('http://127.0.0.1:5000/viewfacility')
    .then((response)=>{
        let facilities = response.data;

    res.render("pages/updatefacility.ejs", {
        facilities: facilities
    });
  });
});

app.post('/formupdatefacility', function(req, res) {
    res.render("pages/success.ejs", {});
    axios.put('http://127.0.0.1:5000/updatefacility', {
        name_to_update: req.body.facnametoupdate,
        new_name: req.body.newfacname
    })
});

app.get('/deletefacility', function(req, res) {
    axios.get('http://127.0.0.1:5000/viewfacility')
    .then((response)=>{
        let facilities = response.data;

    res.render("pages/deletefacility.ejs", {
        facilities: facilities
    });
  });
});

app.post('/formdeletefacility', function(req,res) {
    res.render("pages/success", {});
    const facnametodelete = req.body.facnametodelete
    axios.delete(`http://127.0.0.1:5000/deletefacility?facnametodelete=${facnametodelete}`)
});

app.get('/addclassroom', function(req, res) {
    axios.get('http://127.0.0.1:5000/viewfacility')
    .then((response)=>{
        let facilities = response.data;

    res.render("pages/addclassroom.ejs", {
        facilities: facilities
    });
  });
});

app.post('/formaddclassroom', function(req, res) {
    res.render("pages/success.ejs", {});
    axios.post('http://127.0.0.1:5000/addclassroom', {
        classroomname: req.body.classname,
        new_capacity: req.body.capacity,
        facilityname: req.body.facname
    })
});

app.get('/viewclassroom', function(req, res) {
    axios.get('http://127.0.0.1:5000/viewclassroom')
    .then((response)=>{
        let classrooms = response.data;

        res.render('pages/viewclassroom.ejs', {
            classrooms: classrooms
        });
    });
});

app.get('/updateclassroom', function(req, res) {
    axios.all([axios.get('http://127.0.0.1:5000/viewfacility'), axios.get('http://127.0.0.1:5000/viewclassroom')])
    .then(axios.spread(function(response1, response2) {
        res.render('pages/updateclassroom.ejs', {
            facilities: response1.data,
            classrooms: response2.data
        });
    }));
});
    
app.post('/formupdateclassroom', function(req, res) {
    const classroomtoupdate  = JSON.parse(req.body.classtoupdate)
    res.render("pages/success.ejs", {});
    axios.put('http://127.0.0.1:5000/updateclassroom', {
        classroomname_to_update: classroomtoupdate.classroom_name,
        capacity_to_update: classroomtoupdate.capacity,
        facilityname_to_update: classroomtoupdate.facility_name,
        new_classroomname: req.body.newclassname,
        new_capacity: req.body.newclasscap,
        new_facility: req.body.newclassfac
    });
});

app.get('/deleteclassroom', function(req, res) {
    axios.get('http://127.0.0.1:5000/viewclassroom')
    .then((response)=>{
        let classrooms = response.data;

    res.render("pages/deleteclassroom.ejs", {
        classrooms: classrooms
    });
  });
});

app.post('/formdeleteclassroom', function(req,res) {
    res.render("pages/success", {});
    const classroomtodelete = JSON.parse(req.body.classtodelete)
    axios.delete(`http://127.0.0.1:5000/deleteclassroom?capacity_to_delete=${classroomtodelete.capacity}&classroomname_to_delete=${classroomtodelete.classroom_name}&facilityname_to_delete=${classroomtodelete.facility_name}`)
});

app.get('/addteacher', function(req, res) {
    axios.get('http://127.0.0.1:5000/viewclassroom')
    .then((response)=>{
        let classrooms = response.data;

    res.render("pages/addteacher.ejs", {
        classrooms: classrooms
    });
  });
});

app.post('/formaddteacher', function(req, res) {
    res.render("pages/success.ejs", {});
    const teacherclassroom = JSON.parse(req.body.teacherclass)
    axios.post('http://127.0.0.1:5000/addteacher', {
        new_firstname: req.body.teacherfname,
        new_lastname: req.body.teacherlname,
        capacity: teacherclassroom.capacity,
        roomname: teacherclassroom.classroom_name,
        facilityname: teacherclassroom.facility_name
    })
});

app.get('/viewteacher', function(req, res) {
    axios.get('http://127.0.0.1:5000/viewteacher')
    .then((response)=>{
        let teachers = response.data;

        res.render('pages/viewteacher.ejs', {
            teachers: teachers
        });
    });
});

app.get('/updateteacher', function(req, res) {
    axios.all([axios.get('http://127.0.0.1:5000/viewfacility'), axios.get('http://127.0.0.1:5000/viewclassroom'), axios.get('http://127.0.0.1:5000/viewteacher')])
    .then(axios.spread(function(response1, response2, response3) {
        res.render('pages/updateteacher.ejs', {
            facilities: response1.data,
            classrooms: response2.data,
            teachers: response3.data
        });
    }));
});

app.post('/formupdateteacher', function(req, res) {
    const teachtoupdate  = JSON.parse(req.body.teachertoupdate)
    const newteachroom = JSON.parse(req.body.newroom)
    const factoupdate = JSON.parse(req.body.currentfac)
    const facnew = JSON.parse(req.body.newfac)
    const currentroom = JSON.parse(req.body.currentclass)
    res.render("pages/success.ejs", {});
    axios.put('http://127.0.0.1:5000/updateteacher', {
        firstname_to_update: teachtoupdate.firstname,
        new_firstname: req.body.newfname,
        lastname_to_update: teachtoupdate.lastname,
        new_lastname: req.body.newlname,
        roomname_to_update: teachtoupdate.room,
        new_roomname: newteachroom.classroom_name,
        oldfacilityname: factoupdate.name,
        newfacilityname: facnew.name,
        oldcapacity: currentroom.capacity,
        newcapacity: newteachroom.capacity
    });
});

app.get('/deleteteacher', function(req, res) {
    axios.get('http://127.0.0.1:5000/viewteacher')
    .then((response)=>{
        let teachers = response.data;

    res.render("pages/deleteteacher.ejs", {
        teachers: teachers
    });
  });
});

app.post('/formdeleteteacher', function(req,res) {
    res.render("pages/success", {});
    const teachertodelete = JSON.parse(req.body.teachtodelete)
    axios.delete(`http://127.0.0.1:5000/deleteteacher?firstname_to_delete=${teachertodelete.firstname}&lastname_to_delete=${teachertodelete.lastname}&roomname_to_delete=${teachertodelete.room}`)
});

app.get('/addchild', function(req, res) {
    axios.all([axios.get('http://127.0.0.1:5000/viewfacility'), axios.get('http://127.0.0.1:5000/viewclassroom')])
    .then(axios.spread(function(response1, response2) {
        res.render('pages/addchild.ejs', {
            facilities: response1.data,
            classrooms: response2.data,
        });
    }));
});

app.post('/formaddchild', function(req, res) {
    res.render("pages/success.ejs", {});
    const childclassroom = JSON.parse(req.body.childclass)
    const childfacility = JSON.parse(req.body.childfac)
    axios.post('http://127.0.0.1:5000/addchild', {
        new_firstname: req.body.childfname,
        new_lastname: req.body.childlname,
        new_age: req.body.childage,
        roomname: childclassroom.classroom_name,
        capacity: childclassroom.capacity,
        facilityname: childfacility.name
    })
});

app.get('/viewchild', function(req, res) {
    axios.get('http://127.0.0.1:5000/viewchild')
    .then((response)=>{
        let children = response.data;

        res.render('pages/viewchild.ejs', {
            children: children
        });
    });
});

app.get('/updatechild', function(req, res) {
    axios.all([axios.get('http://127.0.0.1:5000/viewfacility'), axios.get('http://127.0.0.1:5000/viewclassroom'), axios.get('http://127.0.0.1:5000/viewchild')])
    .then(axios.spread(function(response1, response2, response3) {
        res.render('pages/updatechild.ejs', {
            facilities: response1.data,
            classrooms: response2.data,
            children: response3.data
        });
    }));
});

app.post('/formupdatechild', function(req, res) {
    const childupdate  = JSON.parse(req.body.childtoupdate)
    const newchildroom = JSON.parse(req.body.newroom)
    const factoupdate = JSON.parse(req.body.currentfac)
    const facnew = JSON.parse(req.body.newfac)
    const currentroom = JSON.parse(req.body.currentclass)
    res.render("pages/success.ejs", {});
    axios.put('http://127.0.0.1:5000/updatechild', {
        firstname_to_update: childupdate.firstname,
        new_firstname: req.body.newfname,
        lastname_to_update: childupdate.lastname,
        new_lastname: req.body.newlname,
        age_to_update: childupdate.age,
        new_age: req.body.newage,
        roomname_to_update: childupdate.room,
        new_roomname: newchildroom.classroom_name,
        oldfacilityname: factoupdate.name,
        newfacilityname: facnew.name,
        oldcapacity: currentroom.capacity,
        newcapacity: newchildroom.capacity
    });
});

app.get('/deletechild', function(req, res) {
    axios.get('http://127.0.0.1:5000/viewchild')
    .then((response)=>{
        let children = response.data;

    res.render("pages/deletechild.ejs", {
        children: children
    });
  });
});

app.post('/formdeletechild', function(req,res) {
    res.render("pages/success", {});
    const childtodelete = JSON.parse(req.body.childdelete)
    axios.delete(`http://127.0.0.1:5000/deletechild?firstname_to_delete=${childtodelete.firstname}&lastname_to_delete=${childtodelete.lastname}&age_to_delete=${childtodelete.age}&roomname_to_delete=${childtodelete.room}`)
});

app.listen(8080);
console.log('8080 is the magic port');



