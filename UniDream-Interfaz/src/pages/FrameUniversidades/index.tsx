import React from "react";
export default (props) => {
	return (
		<div className="flex flex-col bg-white">
			<div className="self-stretch bg-white pb-6">
				<div className="flex items-center self-stretch bg-[#FFFFFFCC] py-[22px]">
					<img
						src={"https://storage.googleapis.com/tagjs-prod.appspot.com/v1/y0WLx2RbqX/u03asth9_expires_30_days.png"} 
						className="w-[148px] h-[42px] ml-36 mr-10 object-fill"
					/>
					<div className="w-8 h-8 mr-10">
					</div>
					<div className="flex shrink-0 items-center">
						<div className="flex flex-col shrink-0 items-start mr-8">
							<span className="text-[#0D0D1B] text-sm" >
								{"Inicio"}
							</span>
						</div>
						<div className="flex flex-col shrink-0 items-start pb-[1px] mr-8">
							<span className="text-[#0D0D1B] text-sm" >
								{"Carreras"}
							</span>
						</div>
						<div className="flex flex-col shrink-0 items-start pb-[1px] mr-8">
							<span className="text-[#1313EC] text-sm font-bold" >
								{"Universidades"}
							</span>
						</div>
						<div className="flex flex-col shrink-0 items-start pb-[1px] mr-[50px]">
							<span className="text-[#0D0D1B] text-sm" >
								{"Asistente IA"}
							</span>
						</div>
					</div>
				</div>
				<div className="flex flex-col self-stretch max-w-[1152px] mb-12 mx-auto gap-12">
					<div className="flex justify-between items-start self-stretch">
						<div className="flex flex-col shrink-0 items-start gap-4">
							<button className="flex flex-col items-start bg-[#1313EC1A] text-left py-1 px-3 mr-[525px] rounded-[9999px] border-0"
								onClick={()=>alert("Pressed!")}>
								<span className="text-[#1313EC] text-xs font-bold" >
									{"Directorio 2025"}
								</span>
							</button>
							<div className="flex flex-col items-start pb-[1px] pr-32">
								<span className="text-[#0D0D1B] text-5xl font-bold" >
									{"Explora Universidades"}
								</span>
							</div>
							<div className="flex flex-col items-start pb-[1px] pr-11">
								<span className="text-[#4C4C9A] text-lg w-[628px]" >
									{"Utilizamos inteligencia artificial para analizar programas académicos y\nencontrar la institución que mejor se alinea con tus metas profesionales."}
								</span>
							</div>
						</div>
						<div className="flex shrink-0 items-center bg-white py-[13px] px-5 mt-[106px] gap-2 rounded-[9999px] border border-solid border-[#E7E7F3]" 
							style={{
								boxShadow: "0px 1px 2px #0000000D"
							}}>
							<img
								src={"https://storage.googleapis.com/tagjs-prod.appspot.com/v1/y0WLx2RbqX/v6zvajtn_expires_30_days.png"} 
								className="w-5 h-7 rounded-[9999px] object-fill"
							/>
							<div className="flex flex-col shrink-0 items-start pb-[1px]">
								<span className="text-[#0D0D1B] text-base font-bold" >
									{"Filtros Avanzados"}
								</span>
							</div>
						</div>
					</div>
					<div className="flex items-center self-stretch">
						<button className="flex shrink-0 items-center bg-[#1313EC] text-left py-[9px] px-5 mr-[13px] gap-2 rounded-[9999px] border-0" 
							style={{
								boxShadow: "0px 2px 4px #1313EC33"
							}}
							onClick={()=>alert("Pressed!")}>
							<img
								src={"https://storage.googleapis.com/tagjs-prod.appspot.com/v1/y0WLx2RbqX/16w66z7y_expires_30_days.png"} 
								className="w-3.5 h-5 rounded-[9999px] object-fill"
							/>
							<span className="text-white text-sm" >
								{"Recomendadas por AI"}
							</span>
						</button>
						<button className="flex shrink-0 items-center bg-white text-left py-[9px] px-5 mr-3 gap-2 rounded-[9999px] border border-solid border-[#E7E7F3]"
							onClick={()=>alert("Pressed!")}>
							<img
								src={"https://storage.googleapis.com/tagjs-prod.appspot.com/v1/y0WLx2RbqX/sbty664z_expires_30_days.png"} 
								className="w-3.5 h-[19px] rounded-[9999px] object-fill"
							/>
							<span className="text-[#0D0D1B] text-sm" >
								{"Públicas"}
							</span>
						</button>
						<button className="flex shrink-0 items-center bg-white text-left py-[9px] px-5 mr-3 gap-2 rounded-[9999px] border border-solid border-[#E7E7F3]"
							onClick={()=>alert("Pressed!")}>
							<img
								src={"https://storage.googleapis.com/tagjs-prod.appspot.com/v1/y0WLx2RbqX/fvsqjmjg_expires_30_days.png"} 
								className="w-3.5 h-5 rounded-[9999px] object-fill"
							/>
							<span className="text-[#0D0D1B] text-sm" >
								{"Privadas"}
							</span>
						</button>
						<button className="flex shrink-0 items-center bg-white text-left py-[9px] px-5 mr-3 gap-2 rounded-[9999px] border border-solid border-[#E7E7F3]"
							onClick={()=>alert("Pressed!")}>
							<img
								src={"https://storage.googleapis.com/tagjs-prod.appspot.com/v1/y0WLx2RbqX/il8iu3gh_expires_30_days.png"} 
								className="w-3.5 h-5 rounded-[9999px] object-fill"
							/>
							<span className="text-[#0D0D1B] text-sm" >
								{"Ingeniería"}
							</span>
						</button>
						<button className="flex shrink-0 items-center bg-white text-left py-[9px] px-5 gap-2 rounded-[9999px] border border-solid border-[#E7E7F3]"
							onClick={()=>alert("Pressed!")}>
							<img
								src={"https://storage.googleapis.com/tagjs-prod.appspot.com/v1/y0WLx2RbqX/3ns51jb1_expires_30_days.png"} 
								className="w-3.5 h-[19px] rounded-[9999px] object-fill"
							/>
							<span className="text-[#0D0D1B] text-sm" >
								{"Salud"}
							</span>
						</button>
					</div>
					<div className="flex flex-col self-stretch gap-6">
						<div className="flex items-center self-stretch bg-[#F6F9FA] p-[33px] gap-6 rounded-[48px] border border-solid border-[#00000000]">
							<div className="shrink-0 items-start bg-[url('https://storage.googleapis.com/tagjs-prod.appspot.com/v1/y0WLx2RbqX/qyxjr5s3_expires_30_days.png')] bg-cover bg-center pt-[108px] pl-[108px]">
								<div className="bg-green-500 w-5 h-5 rounded-[9999px] border-4 border-solid border-[#F6F6F8]">
								</div>
							</div>
							<div className="flex flex-1 flex-col gap-2">
								<div className="flex items-center self-stretch gap-3">
									<div className="flex flex-col shrink-0 items-start">
										<span className="text-[#0D0D1B] text-2xl font-bold" >
											{"Universidad Nacional de Tecnología"}
										</span>
									</div>
									<button className="flex flex-col shrink-0 items-start bg-[#1313EC0D] text-left py-0.5 px-[9px] rounded-2xl border border-solid border-[#1313EC33]"
										onClick={()=>alert("Pressed!")}>
										<span className="text-[#1313EC] text-[10px] font-bold" >
											{"AI TOP MATCH"}
										</span>
									</button>
								</div>
								<div className="flex flex-col items-start self-stretch">
									<span className="text-[#4C4C9A] text-base" >
										{"Ingeniería y Ciencias Aplicadas • Ciudad de México"}
									</span>
								</div>
								<div className="flex flex-col items-start self-stretch py-[3px] mr-[88px]">
									<span className="text-[#4C4C9A] text-sm w-[588px]" >
										{"Líder en investigación tecnológica con más de 45 programas de ingeniería y convenios\ninternacionales con centros de innovación en Silicon Valley."}
									</span>
								</div>
							</div>
							<div className="flex flex-col shrink-0 items-start gap-3">
								<button className="flex flex-col items-start bg-[#1313EC] text-left py-[11px] px-8 rounded-[9999px] border-0"
									onClick={()=>alert("Pressed!")}>
									<span className="text-white text-sm font-bold" >
										{"Ver Detalles"}
									</span>
								</button>
								<div className="flex items-center gap-1">
									<img
										src={"https://storage.googleapis.com/tagjs-prod.appspot.com/v1/y0WLx2RbqX/bpvj87dm_expires_30_days.png"} 
										className="w-3 h-[15px] object-fill"
									/>
									<span className="text-[#4C4C9A] text-[11px]" >
										{"98% Match con tu perfil"}
									</span>
								</div>
							</div>
						</div>
						<div className="flex items-center self-stretch bg-[#F6F9FA] p-[33px] gap-6 rounded-[48px] border border-solid border-[#00000000]">
							<img
								src={"https://storage.googleapis.com/tagjs-prod.appspot.com/v1/y0WLx2RbqX/e7larkph_expires_30_days.png"} 
								className="w-32 h-32 rounded-[48px] object-fill"
							/>
							<div className="flex flex-1 flex-col gap-2">
								<div className="flex items-center self-stretch gap-3">
									<div className="flex flex-1 flex-col items-start">
										<span className="text-[#0D0D1B] text-2xl font-bold" >
											{"Instituto de Artes y Ciencias"}
										</span>
									</div>
									<button className="flex flex-col shrink-0 items-start bg-orange-100 text-left py-0.5 px-[9px] rounded-2xl border border-solid border-orange-200"
										onClick={()=>alert("Pressed!")}>
										<span className="text-orange-700 text-[10px] font-bold" >
											{"Privada"}
										</span>
									</button>
									<div className="flex-1 h-8">
									</div>
								</div>
								<div className="flex flex-col items-start self-stretch">
									<span className="text-[#4C4C9A] text-base" >
										{"Artes y Humanidades • Guadalajara"}
									</span>
								</div>
								<div className="flex flex-col items-start self-stretch py-[3px] pl-[1px] mr-[86px]">
									<span className="text-[#4C4C9A] text-sm w-[654px]" >
										{"Enfocado en el desarrollo creativo y pensamiento crítico. Ofrece programas exclusivos en Diseño\nDigital, Arquitectura y Bellas Artes."}
									</span>
								</div>
							</div>
							<div className="flex flex-col shrink-0 items-start gap-3">
								<button className="flex flex-col items-start bg-white text-left py-3 px-[33px] rounded-[9999px] border border-solid border-[#1313EC]"
									onClick={()=>alert("Pressed!")}>
									<span className="text-[#1313EC] text-sm font-bold" >
										{"Ver Detalles"}
									</span>
								</button>
								<div className="flex items-center gap-1">
									<img
										src={"https://storage.googleapis.com/tagjs-prod.appspot.com/v1/y0WLx2RbqX/xlwjh6ul_expires_30_days.png"} 
										className="w-3 h-4 object-fill"
									/>
									<span className="text-[#4C4C9A] text-[11px]" >
										{"12k Estudiantes activos"}
									</span>
								</div>
							</div>
						</div>
						<div className="flex items-center self-stretch bg-[#F6F9FA] p-[33px] gap-6 rounded-[48px] border border-solid border-[#00000000]">
							<img
								src={"https://storage.googleapis.com/tagjs-prod.appspot.com/v1/y0WLx2RbqX/aw1r5zfw_expires_30_days.png"} 
								className="w-32 h-32 rounded-[48px] object-fill"
							/>
							<div className="flex flex-1 flex-col gap-2">
								<div className="flex flex-col items-start self-stretch">
									<span className="text-[#0D0D1B] text-2xl font-bold" >
										{"Universidad Metropolitana de Innovación"}
									</span>
								</div>
								<div className="flex flex-col items-start self-stretch">
									<span className="text-[#4C4C9A] text-base" >
										{"Ciencias Sociales y Negocios • Monterrey"}
									</span>
								</div>
								<div className="flex flex-col items-start self-stretch py-[3px] mr-[88px]">
									<span className="text-[#4C4C9A] text-sm w-[568px]" >
										{"Pioneros en el modelo educativo de aprendizaje basado en retos. Especialización en\nemprendimiento y marketing digital."}
									</span>
								</div>
							</div>
							<div className="flex flex-col shrink-0 items-start gap-3">
								<button className="flex flex-col items-start bg-[#1313EC] text-left py-[11px] px-8 rounded-[9999px] border-0"
									onClick={()=>alert("Pressed!")}>
									<span className="text-white text-sm font-bold" >
										{"Ver Detalles"}
									</span>
								</button>
								<div className="flex items-center gap-1">
									<img
										src={"https://storage.googleapis.com/tagjs-prod.appspot.com/v1/y0WLx2RbqX/x8tvbnlp_expires_30_days.png"} 
										className="w-3 h-4 object-fill"
									/>
									<span className="text-[#4C4C9A] text-[11px]" >
										{"85% Match con tu perfil"}
									</span>
								</div>
							</div>
						</div>
					</div>
					<div className="flex flex-col items-center self-stretch pt-4 gap-4">
						<button className="flex items-center bg-[#E7E7F3] text-left py-4 px-[39px] gap-2 rounded-[9999px] border-0"
							onClick={()=>alert("Pressed!")}>
							<img
								src={"https://storage.googleapis.com/tagjs-prod.appspot.com/v1/y0WLx2RbqX/k06r3nsu_expires_30_days.png"} 
								className="w-5 h-7 rounded-[9999px] object-fill"
							/>
							<span className="text-[#0D0D1B] text-base font-bold" >
								{"Cargar más universidades"}
							</span>
						</button>
						<div className="flex flex-col items-start pb-[1px]">
							<span className="text-[#4C4C9A] text-xs" >
								{"Mostrando 3 de 128 instituciones"}
							</span>
						</div>
					</div>
				</div>
				<div className="flex flex-col self-stretch bg-white py-16 mb-6 gap-16">
					<div className="flex flex-col items-center self-stretch max-w-[1200px] mx-auto">
						<div className="flex items-center gap-12">
							<div className="flex flex-col shrink-0 items-start pr-[61px] gap-[15px]">
								<img
									src={"https://storage.googleapis.com/tagjs-prod.appspot.com/v1/y0WLx2RbqX/9yu38t4f_expires_30_days.png"} 
									className="w-[395px] h-[37px] object-fill"
								/>
								<div className="flex flex-col items-start">
									<span className="text-gray-400 text-base w-[319px]" >
										{"Somos un equipo apasionado de estudiantes y\ndesarrolladores comprometidos con\ndemocratizar el acceso a la orientación\nprofesional de calidad mediante el uso\nresponsable de la IA"}
									</span>
								</div>
							</div>
							<div className="flex flex-col shrink-0 items-start pb-[18px]">
								<div className="flex flex-col items-start pb-[1px] pr-[115px]">
									<span className="text-[#0D0D1B] text-base font-bold" >
										{"Plataforma"}
									</span>
								</div>
								<div className="flex flex-col items-start mb-[18px] gap-2">
									<div className="flex flex-col items-start pb-[1px] pr-14">
										<span className="text-[#4C4C9A] text-sm" >
											{"Directorio de Carreras"}
										</span>
									</div>
									<div className="flex flex-col items-start pb-[1px] pr-[29px]">
										<span className="text-[#4C4C9A] text-sm" >
											{"Ranking de Universidades"}
										</span>
									</div>
									<div className="flex flex-col items-start pb-[1px] pr-4">
										<span className="text-[#4C4C9A] text-sm w-[188px]" >
											{"Datos 100% enfocados en el país"}
										</span>
									</div>
									<div className="flex flex-col items-start pb-[1px] pr-44">
										<span className="text-[#4C4C9A] text-sm" >
											{"Blog"}
										</span>
									</div>
								</div>
							</div>
							<div className="flex flex-col shrink-0 items-start pb-[38px]">
								<div className="flex flex-col items-start pb-[1px] pr-[141px]">
									<span className="text-[#0D0D1B] text-base font-bold" >
										{"Soporte"}
									</span>
								</div>
								<div className="flex flex-col items-start mb-[38px] gap-2">
									<div className="flex flex-col items-start pb-[1px] pr-36">
										<span className="text-[#4C4C9A] text-sm" >
											{"Contacto"}
										</span>
									</div>
									<div className="flex flex-col items-start pb-[1px] pr-[178px]">
										<span className="text-[#4C4C9A] text-sm" >
											{"FAQ"}
										</span>
									</div>
									<div className="flex flex-col items-start pb-[1px] pr-[134px]">
										<span className="text-[#4C4C9A] text-sm" >
											{"Privacidad"}
										</span>
									</div>
									<div className="flex flex-col items-start pb-[1px] pr-[145px]">
										<span className="text-[#4C4C9A] text-sm" >
											{"Términos"}
										</span>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div className="flex items-start self-stretch mx-[11px] gap-8">
						<div className="w-[77px] h-[15px] mt-[35px]">
						</div>
						<div className="flex flex-1 flex-col items-start pt-[38px] pl-[121px]">
							<span className="text-gray-500 text-sm" >
								{"© 2026 UniDream Platform. Todos los derechos reservados. Diseñado para el éxito estudiantil."}
							</span>
						</div>
						<div className="flex flex-col shrink-0 items-start mt-[35px]">
							<span className="text-[#4C4C9A] text-[10px] font-bold" >
								{"Privacidad"}
							</span>
						</div>
					</div>
				</div>
			</div>
		</div>
	)
}