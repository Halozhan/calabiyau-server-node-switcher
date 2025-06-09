namespace Core.HostsManager
{
    internal class HostsParser
    {
        // 텍스트를 Host 리스트로 파싱
        public static List<(string, Host?)> ParseTextToHostsList(string[] lines)
        {
            List<(string, Host?)> parsedLines = [];
            
            foreach (var line in lines)
            {
                // 주석과 공백 라인 유지
                if (string.IsNullOrWhiteSpace(line) || line.StartsWith('#'))
                {
                    parsedLines.Add((line, null));
                    continue;
                }

                // IP 주소와 도메인으로 나누기
                string[] parts = line.Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries);
                if (parts.Length == 2)
                {
                    // IP 주소와 도메인이 있는 경우 Host 객체 생성
                    parsedLines.Add((line, new Host(parts[0], parts[1])));
                }
                else
                {
                    // IP 주소와 도메인이 없는 경우 Host 객체 생성하지 않음
                    parsedLines.Add((line, null));
                }
            }

            return parsedLines;
        }

        // Host 리스트를 텍스트로 직렬화
        public static string[] SerializeHostsListToText(List<(string, Host?)> parsedLines)
        {
            string[] serializedLine = new string[parsedLines.Count];
            for (int i = 0; i < parsedLines.Count; i++)
            {
                serializedLine[i] = parsedLines[i].Item2 == null ? parsedLines[i].Item1 : $"{parsedLines[i].Item2.IP}\t{parsedLines[i].Item2.Hostname}";
            }

            return serializedLine;
        }
    }
}
