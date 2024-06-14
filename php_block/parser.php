<?php
require_once __DIR__ . DIRECTORY_SEPARATOR . 'phpQuery.php';

class Parser
{
    const PATH = 'json/tableData.json';
    const HREF_PATH = 'json/hrefTable.json';
    private $URL = null;

    private function setURL() {
        if (file_exists(self::HREF_PATH)) {
            $url = json_decode(file_get_contents(self::HREF_PATH), true);
            $this->URL = $url;
        }
    }

    private function getDOM() : ?string
    { 
        $ch = curl_init($this->URL);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        $html = curl_exec($ch);
        curl_close($ch);
        return $html;
    }

    private function parseDOM($html) : array 
    {
        $dom = phpQuery::newDocument($html);
        $table = $dom->find('table.waffle tbody');
        $items = [];
        foreach ($table->find('tr') as $row) {
            $item = [];
            foreach (pq($row)->find('td') as $col) {
                $item[] = pq($col)->text();
            }
            $items[] = $item;
        }
        return $items;
    }

    private function createJSON(array $data) : void
    {
        file_put_contents(self::PATH, json_encode($data, JSON_UNESCAPED_UNICODE));
    }

    public function parse()
    {
        $this->setURL();
        if ($this->URL) {
            $html = $this->getDOM();
            if ($html) {
                $items = $this->parseDOM($html);
                $this->createJSON($items);
            }
        }
    }
}

$parser = new Parser();
$parser->parse();
