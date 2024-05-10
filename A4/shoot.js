


        
$(document).ready(function() {
    console.log("Document ready!");

    // Define variables for global use within this scope
    var cueBall = $('svg circle[fill="WHITE"]');
    var cue = $('svg line');
    var table = $('svg');
    var isDrawing = false; // Use false instead of False
    var startX, startY;

    // Function to handle form submission
    // function handleFormSubmission() {
    //     alert("enter the handle form")
    //     $('form').on('submit', function(event) {
    //         console.log("Form submitted.");
    //         event.preventDefault(); // Prevent the actual form submission

    //         // Perform the POST request
    //         $.post('/display.html', $(this).serialize(), function(svgMarkup) {
    //             console.log("Received SVG:", svgMarkup); // Log the SVG markup
    //             // Insert the SVG markup into the 'svg-container' div
    //             $('#svg-container').html(svgMarkup);
    //         }).fail(function(jqXHR, textStatus, errorThrown) {
    //             console.log("Failed to load SVG:", textStatus, errorThrown); // Log the error
    //             $('#svg-container').text('Failed to load SVG.');
    //         });
    //     });
    // }

    // Function to handle mouse events for drawing
    function eventHandler() {
    var cueBall = $('svg circle[fill="WHITE"]');
    var cue = $('svg line');
    var table = $('svg');
    var isDrawing = false; // Use false instead of False

        
        cueBall.on('mousedown', function(e) {
            
            isDrawing = true;
            var ballPosition = $(this).position();
            startX = ballPosition.left + $(this).width() / 2; // Assuming the x1 and y1 attributes represent the center of the cue ball
            startY = ballPosition.top + $(this).height() / 2;
            console.log('MouseDown - Drawing started. Initial Position:', cueBall.attr("cx"), cueBall.attr("cy"));

            cue.attr({
                'x1': cueBall.attr("cx"),
                'y1': cueBall.attr("cy"),
                'x2': cueBall.attr("cx"),
                'y2': cueBall.attr("cy")
            })
            
            cue.show();
            
        });

        $(document).on('mousemove', function(e) {
            
            if (!isDrawing) return;
            
            console.log( 'in mouse move ')

            const { clientX, clientY } = e;
            const { left, top } = table.offset();
            const svgWidth = table.width();
            const svgHeight = table.height();
            const viewBoxWidth = 1400;
            const viewBoxHeight = 2750;

            const scaledX = ((clientX - left) / svgWidth) * viewBoxWidth;
            const scaledY = ((clientY - top) / svgHeight) * viewBoxHeight;

            cue.attr('x2', scaledX).attr('y2', scaledY);
            console.log('MouseMove - Current Position:', { scaledX, scaledY });
        });

        $(document).on('mouseup', function(e) {
            if (isDrawing) {
                cue.hide();
                isDrawing = false;
                console.log('MouseUp - Drawing ended.');

            const {clientX, clientY} = e
            
            const { left, top } = table.offset();
            const svgWidth = table.width();
            const svgHeight = table.height();
            const viewBoxWidth = 1400;
            const viewBoxHeight = 2750;
            const releaseX = ((clientX - left) / svgWidth) * viewBoxWidth;
            const releaseY = ((clientY - top) / svgHeight) * viewBoxHeight;

            // Calculate velocity vector
            const velocityX = (releaseX - cueBall.attr("cx")) * -2.5;
            const velocityY = (releaseY - cueBall.attr("cy")) * -2.5;

            console.log('Velocity:', { x: velocityX, y: velocityY });
            const data = {
                velocityX: velocityX.toString(),
                velocityY: velocityY.toString()
            };
    
            // AJAX POST request to server with velocity data
            $.ajax({
                url: '/process_velocity',  // Update this URL to your server's endpoint that processes velocity
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(data),
                success: function(svgs) {
                    console.log('Server response:', typeof(svgs));
                    let iteration = 0

                    function process() {
                        if (iteration < svgs.length) {
                            let item = svgs[iteration];
                            // alert("enetered iterator")
            
                            // Replace previous svg
                            $("svg").replaceWith(item);
                            eventHandler();
            
                            iteration++;
                            setTimeout(process, 10);
                    }
                }
                    process()
                },
                error: function(error) {
                    console.log('Error:', error);
                }
            });
        }
            

    });
       
    }

    // Call the functions to set up event handler
    eventHandler();
});

        





