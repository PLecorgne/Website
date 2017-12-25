function main() {
    // Initially hide toggleable content
    $("tr.info-row").find("p").hide();

      // Click handler on entire table
    $("table").click(function(event) {

          // No bubbling up
        event.stopPropagation();

        var $target = $(event.target);

          // Open and close the appropriate thing
        if ( $target.closest("tr").attr("colspan") > 1 ) {
            $target.slideUp();
        } else {
            $target.closest("tr").next().find("p").slideToggle();
        }
    });
}

$(document).ready(main());
