# 📅 Eventos Python no Brasil

![image](https://static.wikia.nocookie.net/bttf/images/d/d5/Time_Circuits_BTTF.png)

## Como adicionar um novo evento na agenda?

Para adicionar um evento/meetup/conferência/etc na agenda, basta seguir os passos abaixo:

### 1. Forkar esse repositório

O primeiro passo é criar um `fork` desse respositório na sua conta do Github. Se você não sabe como fazer isso, você pode seguir um dos [guias[1]](https://help.github.com/articles/fork-a-repo/) [oficias[2]](https://guides.github.com/activities/forking/) do Github em inglês, ou pode dar uma olhada no texto que a [leportella](http://leportella.com) escreveu sobre [como contribuir com projetos open source[3]](http://leportella.com/pt-br/2017/04/17/como-contribuir-com-open-source.html).

### 2. Adicionar novo evento na agenda

Para adicionar um novo evento na agenda e no site [eventos.python.org.br](https://eventos.python.org.br), basta alterar o arquivo `conferencias.toml` com os dados do seu evento. É preciso preencher nome, data que o evento começa e termina no padrão yyyy-mm-dd, local onde vai acontecer e url do site. Você pode usar o modelo abaixo como exemplo:

```toml
[[events]]
name = "PyConBrasil 2006"
start = 2006-06-01
end = 2006-06-02
location = "Brasília, DF"
url = "https://manual-do-big-kahuna.readthedocs.io/en/latest/historia/pyconbrasil2.html"
```

### 3. Fazer um pull request com as alterações

Pronto, agora basta fazer um pull request com as suas mudanças, quando o PR for revisado e aceito, o novo evento deverá aparecer na [agenda](https://calendar.google.com/calendar/embed?src=rougeth.com_5a9t9ilqlfumkopl3nlmmkq9kk%40group.calendar.google.com&ctz=America%2FSao_Paulo) e no site [eventos.python.org.br](https://eventos.python.org.br).
