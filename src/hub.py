# from reactpy import component, html, backend

# # Homepage component with scroll-controlled video
# @component
# def Hub():
#     return html.div(
#         {},
#         html.h1("Welcome to the Homepage"),
#         html.p("Scroll up to play backward, scroll down to play forward."),
#         # Link to another page or section (use any route you want)
#         html.a(
#             {"href": "#", "style": {"color": "blue", "textDecoration": "underline"}},
#             "Go to Video Page"
#         ),
#         # Video element with controls and a scroll event
#         html.video(
#             {"id": "video", "style": {"width": "100%", "display": "block", "margin": "auto"}},
#             html.source({"src": "http://localhost:8001/videos/home/video1.mp4", "type": "video/mp4"})
#         ),
#         # Script for handling scroll-based video control
#         html.script("""
#             const video = document.getElementById('video');
#             let lastScrollPosition = window.scrollY;

#             // This threshold controls the sensitivity of scroll
#             const scrollThreshold = 5; // Adjust this value to make scrolling more/less sensitive
#             let isScrolling = false;

#             function scrollHandler() {
#                 const currentScroll = window.scrollY;

#                 if (Math.abs(currentScroll - lastScrollPosition) > scrollThreshold) {
#                     if (currentScroll > lastScrollPosition) {
#                         // Scroll down, play video forward continuously
#                         video.currentTime += 0.1;  // Play forward frame-by-frame
#                     } else if (currentScroll < lastScrollPosition) {
#                         // Scroll up, play video backward continuously
#                         video.currentTime -= 0.1;  // Play backward frame-by-frame
#                     }

#                     // Update the last scroll position
#                     lastScrollPosition = currentScroll;
#                 }

#                 // Set a delay to avoid excessive events
#                 if (!isScrolling) {
#                     isScrolling = true;
#                     setTimeout(() => {
#                         isScrolling = false;
#                     }, 50);
#                 }
#             }

#             // Listen for scroll events and handle them
#             window.addEventListener('scroll', scrollHandler);
#         """)
#     )

from reactpy import component, html, backend

# Homepage component with scroll-controlled video
@component
def Hub():
    return html.div(
        {},
        html.h1("Welcome to the Homepage"),
        html.p("Scroll up to play backward, scroll down to play forward."),
        # Link to another page or section (use any route you want)
        html.a(
            {"href": "#", "style": {"color": "blue", "textDecoration": "underline"}},
            "Go to Video Page"
        ),
        # Video element with controls and a scroll event
        html.video(
            {"id": "video", "style": {"width": "100%", "height": "100vh", "objectFit": "cover", "display": "block", "margin": "auto"}},
            html.source({"src": "http://localhost:8001/videos/home/video1.mp4", "type": "video/mp4"})
        ),
        # Script for handling scroll-based video control
        html.script("""
            const video = document.getElementById('video');
            let isScrolling = false;

            // Constants for video frame control
            const FPS = 30;  // Assuming 30fps video (1 frame = 1/30th of a second)
            const frameStep = 1 / FPS;  // 1 frame forward/backward per scroll
            const scrollSpeed = 0.3;  // Speed multiplier for video scroll (adjust to control frame change rate)
            let lastWheelTime = 0;

            // This will ensure video doesn't go out of bounds
            function updateVideoTime(newTime) {
                if (newTime < 0) {
                    newTime = 0;
                } else if (newTime > video.duration) {
                    newTime = video.duration;
                }
                video.currentTime = newTime;
            }

            function wheelHandler(event) {
                event.preventDefault();  // Prevent default scroll behavior

                const currentTime = Date.now();
                if (currentTime - lastWheelTime < 16) {  // Limit to about 60fps for smoothness
                    return;
                }
                lastWheelTime = currentTime;

                // Handle scroll direction: wheelDelta determines if scrolling up/down
                let newTime = video.currentTime;

                if (event.deltaY > 0) {
                    // Scroll down, move forward by one frame
                    newTime += frameStep * scrollSpeed;
                } else {
                    // Scroll up, move backward by one frame
                    newTime -= frameStep * scrollSpeed;
                }

                // Update video time ensuring it doesn't go out of bounds
                updateVideoTime(newTime);
            }

            // Listen for wheel events and handle them
            window.addEventListener('wheel', wheelHandler, { passive: false });
        """)
    )
