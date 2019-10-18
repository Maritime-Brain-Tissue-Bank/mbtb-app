$(document).ready(function () {
    //sample json data
    var jsondata = [
        {
            "DateTimeRequest": "1",
            "First Name": "first name1",
            "Middle Name": "Name1",
            "Last Name": "name1",
            "Email": "email1",
            "Institution": "ins1",
            "Department": "dep1",
            "Position": "pos1",
            "Address 1": "add1",
            "Address 2": "add2",
            "Country": "coun1",
            "Province": "prov1",
            "Zip code": "code1"
        },
        {
            "DateTimeRequest": "2",
            "First Name": "first name2",
            "Middle Name": "Name2",
            "Last Name": "name2",
            "Email": "email2",
            "Institution": "ins2",
            "Department": "dep2",
            "Position": "pos2",
            "Address 1": "add2",
            "Address 2": "add2",
            "Country": "coun2",
            "Province": "prov2",
            "Zip code": "code2"
        },
        {
            "DateTimeRequest": "3",
            "First Name": "first name3",
            "Middle Name": "Name3",
            "Last Name": "name3",
            "Email": "email3",
            "Institution": "ins3",
            "Department": "dep3",
            "Position": "pos3",
            "Address 1": "add3",
            "Address 2": "add3",
            "Country": "coun3",
            "Province": "prov3",
            "Zip code": "code3"
        },
        {
            "DateTimeRequest": "4",
            "First Name": "first name4",
            "Middle Name": "Name4",
            "Last Name": "name4",
            "Email": "email4",
            "Institution": "ins4",
            "Department": "dep4",
            "Position": "pos4",
            "Address 1": "add4",
            "Address 2": "add4",
            "Country": "coun4",
            "Province": "prov4",
            "Zip code": "code4"
        },
        {
            "DateTimeRequest": "5",
            "First Name": "fist name5",
            "Middle Name": "Name5",
            "Last Name": "name5",
            "Email": "email5",
            "Institution": "ins5",
            "Department": "dep5",
            "Position": "pos5",
            "Address 1": "add5",
            "Address 2": "add5",
            "Country": "coun5",
            "Province": "prov5",
            "Zip code": "code5"
        }
    ];
    $('#table').bootstrapTable(
        {
            data: jsondata
        }
    );
    /* using data-url：*/
    /* $table.bootstrapTable('refresh', {
         url: 'url'
     });*/


});