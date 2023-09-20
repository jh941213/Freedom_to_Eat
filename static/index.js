function btnUploadImage() {
	const fileInput = document.getElementById("fileUpload")

	const handleFiles = (e) => {
		const selectedFile = [...fileInput.files]
		const fileReader = new FileReader()

		fileReader.readAsDataURL(selectedFile[0])

		fileReader.onload = function () {
			document.getElementById("previewImg").src = fileReader.result
		}
	}

	fileInput.addEventListener("change", handleFiles)
}

function btnShootImage() {
	window.location.replace("{{ url_for('select') }}")
}

var ingredients = []

$(document).ready(function () {
	//파일첨부 이벤트
	$("#btnUploadImage").on("change", function () {
		if (window.FileReader) {
			var filename = $(this).children()[0].files[0].name
			if (!validFileType(filename)) {
				alert("허용하지 않는 확장자 파일입니다.")
				return false
			} else {
				if (!validFileSize($(this).children()[0].files[0])) {
					alert("파일 사이즈가 10MB를 초과합니다.")
					return false
				} else {
					if (!validFileNameSize(filename)) {
						alert("파일명이 30자를 초과합니다.")
						return false
					}
				}
			}
		} else {
			var filename = $(this).val().split("/").pop().split("\\").pop()
		}
		// $(this).prev().val(filename) //input upload-name 에 파일명 설정해주기
		readImage($(this).children()[0]) //미리보기

		// 이미지 전달하기
		callYolo()
	})

	$(document).on("click", ".tag-x", function () {
		// 현재 text
		current_text = $($(this).parent().children()[0]).text()
		// 현재 text 배열에 없애기.
		const index = ingredients.indexOf(current_text)
		if (index > -1) {
			// only splice array when item is found
			ingredients.splice(index, 1) // 2nd parameter means remove one item only
		}
		// 태그 삭제
		$(this).parent().remove()
	})

	$("#name").on("keydown", function (key) {
		if (key.keyCode == 13) {
			current_class = [$(this).val()]
			addTags(current_class)
			$(this).val("")
			key.stopImmediatePropagation()
		}
	})
})

function callYolo() {
	// previewImg 에 보여줬던 이미지 전달해서
	// 라벨 받아오기
	// 받아온 라벨 textbox 에 뿌리기

	var fd = new FormData()
	var files = $("#file1")[0].files[0]
	fd.append("file", files)

	$.ajax({
		url: "callYolo",
		type: "post",
		// accept: "application/json",
		// contentType: "application/json; charset=utf-8",
		data: fd,
		contentType: false,
		processData: false,
		success: function (data) {
			console.log(data)
			if (data.result == "success") {
				clearTags()
				addTags(data.classes)
			}
		},
		error: function (jqXHR, textStatus, errorThrown) {
			console.log(jqXHR)
		},
	})
}

function clearTags() {
	$("#tags").html("")
}

function addTags(tags) {
	// 초기화
	// $("#tags").html("")
	$("#tags").removeClass("tags-2")
	$("#tags").addClass("tag")

	var tagsHtml = $("#tags").html()
	console.log(tags)
	for (i = 0; i < tags.length; i++) {
		console.log(tags[i])
		// tags 안에 추가하기
		tagsHtml += "<div class='tag-label'><div class='tag-inner'>";
		tagsHtml += tags[i];
		var xcrossPath = "/static/xcross.svg";  // Flask static 폴더 내의 실제 경로
		tagsHtml += "</div><div class='tag-x'><img src='" + xcrossPath + "' class='xcross-icon'></div></div>";
		ingredients.push(tags[i]);
	}

	$("#tags").html(tagsHtml);
}

function validFileType(filename) {
	const fileTypes = ["png", "jpg", "jpeg"]
	return (
		fileTypes.indexOf(
			filename
				.substring(filename.lastIndexOf(".") + 1, filename.length)
				.toLowerCase()
		) >= 0
	)
}

function validFileSize(file) {
	if (file.size > 10000000) {
		//10MB
		return false
	} else {
		return true
	}
}

function validFileNameSize(filename) {
	if (filename.length > 30) {
		//30자
		return false
	} else {
		return true
	}
}

//이미지 띄우기
function readImage(input) {
	if (input.files && input.files[0]) {
		const reader = new FileReader()
		reader.onload = function (e) {
			const previewImage = document.getElementById("previewImg")
			previewImage.src = e.target.result
			if (
				document
					.getElementById("previewImg")
					.classList.contains("image")
			) {
				document.getElementById("previewImg").classList.remove("image")
			}
			// video 하다가 다시 돌아왔을 때.
			if (
				document
					.getElementById("previewImg")
					.classList.contains("image-3")
			) {
				document
					.getElementById("previewImg")
					.classList.remove("image-3")
			}
			// video display none
			// video display none
			if (document.getElementById("video").classList.contains("video")) {
				document.getElementById("video").classList.remove("video")
				document.getElementById("video").classList.add("video-2")
			}
			// 버튼 사진 재촬영으로 바꿔주기.
			if (
				document
					.getElementById("btnShootImage")
					.classList.contains("button")
			) {
				document
					.getElementById("btnShootImage")
					.classList.remove("button")
				document
					.getElementById("btnShootImage")
					.classList.add("button-2")
				document
					.getElementById("btnShootStart")
					.classList.remove("button-2")
				document.getElementById("btnShootStart").classList.add("button")
			}

			document.getElementById("previewImg").classList.add("image-2")
		}
		// reader가 이미지 읽도록 하기
		reader.readAsDataURL(input.files[0])
	}
}

//이미지 원본 팝업 띄우기
function popImage(url) {
	var img = new Image()
	img.src = url
	var img_width = img.width
	var win_width = img.width + 25
	var img_height = img.height
	var win = img.height + 30
	var popup = window.open(
		"",
		"_blank",
		"width=" +
			img_width +
			", height=" +
			img_height +
			", menubars=no, scrollbars=auto"
	)
	popup.document.write(
		"<style>body{margin:0px;}</style><img src='" +
			url +
			"' width='" +
			win_width +
			"'>"
	)
}

var streaming = false
var video = null
var canvas = null
var photo = null
var startbutton = null

var width = 320 // We will scale the photo width to this
var height = 0 // This will be computed based on the input stream

function clickShootStart() {
	// 버튼 바꿔주기
	// 기존 버튼 안보이게
	// btnShootImage 보이게
	if (document.getElementById("btnShootStart").classList.contains("button")) {
		document.getElementById("btnShootStart").classList.remove("button")
		document.getElementById("btnShootStart").classList.add("button-2")
		document.getElementById("btnShootImage").classList.remove("button-2")
		document.getElementById("btnShootImage").classList.add("button")
	}

	// 비디오 display: none 해제
	if (document.getElementById("video").classList.contains("video-2")) {
		document.getElementById("video").classList.remove("video-2")
		document.getElementById("video").classList.add("video")
	}

	video = document.getElementById("video")
	canvas = document.getElementById("canvas")
	photo = document.getElementById("previewImg")
	startbutton = document.getElementById("btnShootImage")

	navigator.mediaDevices
		.getUserMedia({
			video: true,
			audio: false,
		})
		.then(function (stream) {
			video.srcObject = stream
			video.play()
		})
		.catch(function (err) {
			console.log("An error occurred: " + err)
		})

	video.addEventListener(
		"canplay",
		function (ev) {
			if (!streaming) {
				height = video.videoHeight / (video.videoWidth / width)

				if (isNaN(height)) {
					height = width / (4 / 3)
				}

				video.setAttribute("width", width)
				video.setAttribute("height", height)
				canvas.setAttribute("width", width)
				canvas.setAttribute("height", height)
				streaming = true
			}
		},
		false
	)

	startbutton.addEventListener(
		"click",
		function (ev) {
			takepicture()
			ev.preventDefault()
		},
		false
	)

	clearphoto()
}

function clearphoto2() {
	var context = canvas.getContext("2d")
	context.fillStyle = "#AAA"
	context.fillRect(0, 0, canvas.width, canvas.height)

	var data = canvas.toDataURL("image/png")
	photo.setAttribute("src", data)
}

function clearphoto() {
	// previewImg 숨기기
	if (document.getElementById("previewImg").classList.contains("image-2")) {
		document.getElementById("previewImg").classList.remove("image-2")
	}
	if (document.getElementById("previewImg").classList.contains("image")) {
		document.getElementById("previewImg").classList.remove("image")
	}
	document.getElementById("previewImg").classList.add("image-3")
}

function takepicture() {
	var context = canvas.getContext("2d")
	if (width && height) {
		canvas.width = width
		canvas.height = height
		context.drawImage(video, 0, 0, width, height)

		var data = canvas.toDataURL("image/png")
		photo.setAttribute("src", data)

		// previewImg 다시 display
		if (
			document.getElementById("previewImg").classList.contains("image-3")
		) {
			document.getElementById("previewImg").classList.remove("image-3")
		}
		document.getElementById("previewImg").classList.add("image-2")

		// video display none
		if (document.getElementById("video").classList.contains("video")) {
			document.getElementById("video").classList.remove("video")
			document.getElementById("video").classList.add("video-2")
		}

		callYolo2()
	} else {
		clearphoto()
	}

	// button 바꿔주기
	if (
		document.getElementById("btnShootStart").classList.contains("button-2")
	) {
		document.getElementById("btnShootStart").classList.remove("button-2")
		document.getElementById("btnShootStart").classList.add("button")
		document.getElementById("btnShootImage").classList.remove("button")
		document.getElementById("btnShootImage").classList.add("button-2")
	}
}

function clickToSelect() {
	// window.location.replace("{{ url_for('select') }}")
	// ingredients 전달하기
	var ingredients_value = ""
	for (var i = 0; i < ingredients.length; i++) {
		ingredients_value += ingredients[i] + ", "
	}
	if (ingredients_value.length > 0) {
		ingredients_value = ingredients_value.slice(0, -2)
	}
	$("#ingredients").val(ingredients_value)

	return true
}

function callYolo2() {
	// previewImg 에 보여줬던 이미지 전달해서
	// 라벨 받아오기
	// 받아온 라벨 textbox 에 뿌리기

	// var fd = new FormData()
	// var files = $("#previewImg").attr("src")
	// fd.append("file", files)

	canvas.toBlob(function (blob) {
		const fd = new FormData()
		fd.append("file", blob, "filename.png")

		$.ajax({
			url: "callYolo",
			type: "post",
			// accept: "application/json",
			// contentType: "application/json; charset=utf-8",
			data: fd,
			contentType: false,
			processData: false,
			success: function (data) {
				console.log(data)
				if (data.result == "success") {
					clearTags()
					addTags(data.classes)
				}
			},
			error: function (jqXHR, textStatus, errorThrown) {
				console.log(jqXHR)
			},
		})
	})
}
