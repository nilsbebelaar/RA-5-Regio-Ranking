function toggleRows(color) {
    const e = 'table.ranking tr.detail.' + color
    if ($(e).is(':visible')) {
        $(e).fadeToggle(250) 
    } else {
        $(e).fadeToggle(250) 
    };
}
