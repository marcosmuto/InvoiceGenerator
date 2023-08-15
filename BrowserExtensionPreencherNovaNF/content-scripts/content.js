function enter_value(field_name, field_value) {
	var field = document.getElementById(field_name);
	field.value = field_value;
}

var values_url = chrome.runtime.getURL("data.json");
fetch(values_url)
	.then((response) => response.json())
	.then((json) => {
		enter_value("ctl00_body_tbRazaoSocial", json.razao);
		enter_value("ctl00_body_tbLogradouro", json.logradouro);
		enter_value("ctl00_body_tbDiscriminacao", json.discriminacao);
		enter_value("ctl00_body_tbServEncerradoCodigo", json.codigo_servico);
		enter_value("ctl00_body_tbValor", json.valor);
		}
	);
