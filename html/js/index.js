/**
 * Created by lin on 2020/12/7.
 */

var data = {
    "name": "test",
    "age": 1
}
$.ajax({
    type: 'POST',
    url:/message,
    data: JSON.stringify(data),
    contentType: 'application/json; charset=UTF-8',
    dataType: 'json',
    success: function(data) {

    },
    error: function(xhr, type) {
    }
});
