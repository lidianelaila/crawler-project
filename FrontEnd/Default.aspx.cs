// using Newtonsoft.Json;
// using System;
// using System.Collections.Generic;
// using System.Net;
// using System.Net.Http;
// using System.Net.Http.Headers;
// using System.Text;

// namespace ProjetoPesquisaTextos
// {
//     public partial class Default : System.Web.UI.Page
//     {
//         protected void Page_Load(object sender, EventArgs e)
//         {
//             TxtPesquisa.Focus();
//         }

//         private static string EnderecoURL = "http://127.0.0.1:5000/";

//         protected void PnlResultado_Callback(object sender, DevExpress.Web.CallbackEventArgsBase e)
//         {
//             using (var client = new HttpClient())
//             {
//                 dynamic sb = new StringBuilder();

//                 try
//                 {
//                     client.DefaultRequestHeaders.Accept.Clear();
//                     client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
//                     client.DefaultRequestHeaders.UserAgent.Add(new ProductInfoHeaderValue("Mozilla", "5.0"));

//                     ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12 | SecurityProtocolType.Tls11 | SecurityProtocolType.Tls;

//                     HttpResponseMessage resposta = client.GetAsync(string.Concat(EnderecoURL, e.Parameter)).GetAwaiter().GetResult();

//                     if (resposta.StatusCode == HttpStatusCode.OK)
//                     {
//                         string conteudo = resposta.Content.ReadAsStringAsync().GetAwaiter().GetResult();
//                         List<RetornoWS> Resultado = JsonConvert.DeserializeObject<List<RetornoWS>>(conteudo);

//                         if (Resultado.Count == 0)
//                         {
//                             sb.Append("<p class='text-muted mt-2'>Ooops... nenhum resultado encontrado</p>");
//                             DivConteudo.InnerHtml = Convert.ToString(sb);
//                         }
//                         else
//                         {
//                             //sb.Append("<div class='table-responsive float-left'>");
//                             sb.Append("<table class='table table-striped table-centered mb-0'>");
//                             sb.Append("<tbody>");

//                             foreach (RetornoWS Parte in Resultado)
//                             {
//                                 sb.Append("<tr>");
//                                 sb.Append("<td>");
//                                 sb.Append("<p class='text-left'><b>" + Parte.url + "</b></p>");
//                                 sb.Append("<p class='text-left'>" + Parte.paragrafo + "</p>");
//                                 sb.Append("</td>");
//                                 sb.Append("<td>");
//                                 sb.Append("<span class='text-muted font-13'>" + Math.Round(Parte.nota, 2) + "</span>");
//                                 sb.Append("</td>");
//                                 sb.Append("</tr>");
//                             }
//                             sb.Append("</tbody>");
//                             sb.Append("</tdtable>");

//                             DivConteudo.InnerHtml = Convert.ToString(sb);
//                         }
//                     }
//                     else
//                     {
//                         sb.Append("<p class='text-muted mt-2'>Ooops... erro interno no WS</p>");
//                         DivConteudo.InnerHtml = Convert.ToString(sb);
//                     }
//                 }
//                 catch
//                 {
//                     sb.Append("<p class='text-muted mt-2'>Ooops... nenhum resultado encontrado</p>");
//                     DivConteudo.InnerHtml = Convert.ToString(sb);
//                 }
//             }
//         }

//         public class RetornoWS
//         {
//             public decimal nota { get; set; }
//             public string paragrafo { get; set; }
//             public string url { get; set; }
//         }
//     }
// }