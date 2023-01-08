const fileInput = document.querySelector("#file-input");
const wrapper = document.querySelector(".wrapper");
const fileName = document.querySelector(".file-name");
const defaultBtn = document.querySelector("#default-btn");
const customBtn = document.querySelector("#custom-btn");
const cancelBtn = document.querySelector("#cancel-btn i");
const searchBtn = document.querySelector("#search-btn");
const img = document.querySelector("#img_preview");

  
function defaultBtnActive(){
    defaultBtn.click();
    }

defaultBtn.addEventListener("change", function(){
    const file = this.files[0];
    setPreviewImg(file);

});

window.addEventListener("paste", e=>
{
    if(e.clipboardData.files.length > 0)
    {
        //fileInput.files = e.clipboardData.files;
        if(e.clipboardData.files[0].type.startsWith("image/"))
        {
            setPreviewImg(e.clipboardData.files[0]);
        }
    }
}
);

function setPreviewImg(file) {  
        if(file){
        const reader = new FileReader();
        reader.onload = function(){
        const result = reader.result;
        img.src = result;
        wrapper.classList.add("active");
        }
        cancelBtn.addEventListener("click", function(){
            img.src = "";
            wrapper.classList.remove("active");
            })
            reader.readAsDataURL(file);
                }
        
};

const saveImage = (e) => {
    const link = document.createElement("a"); // creating <a> element
    const img_canvas = document.createElement("canvas");
    img_canvas.width = e.target.naturalWidth;
    img_canvas.height = e.target.naturalHeight;
    img_canvas.getContext("2d").drawImage(e.target,0,0,img_canvas.width,img_canvas.height);
    link.href = img_canvas.toDataURL();  

    link.download = "image.jpg";
    link.click();
};

const sendData = () => {

    let formData = new FormData();
	formData.append('imageBase64' , img.src);
    const imgExists = document.querySelectorAll(
        '.images'
       ).length > 0;
    if(imgExists){
        const image_prev = document.querySelectorAll('.images');
        image_prev.forEach(img_prev => {
            img_prev.remove();
          });
    }
    $.ajax({
        type: "POST",
        url: "imgSearch",
        data:formData,
    
        processData: false,
        contentType: false,
        error: function(data){
            console.log("upload error" , data);
            console.log(data.getAllResponseHeaders());
        },
        success: function(data){
            console.log('success');
            $('#targetLayer').show();
            $('#targetLayer').append(data.htmlresponse);
            const img_list = document.querySelectorAll(".images img");
            img_list.forEach( ind => ind.addEventListener("click",saveImage));
        }
      
      })
}
customBtn.addEventListener("click", defaultBtnActive);
searchBtn.addEventListener("click",sendData)